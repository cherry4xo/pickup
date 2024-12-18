use actix_web::HttpRequest;
use std::str::FromStr;
use uuid::Uuid;
use std::vec::Vec;

use crate::errors::Errors;
use crate::models::entities::{users, users::Entity as Users};
use crate::schemas::token::{TokenBodyResponse, UserToken};
use crate::schemas::users::{UserGet, UserLogin};
use crate::utils::hash;
use crate::utils::token::{is_auth_header_valid, decode_token};
use crate::constants;
use crate::utils::verify_password;
use sea_orm::*;

pub struct Query;

impl Query {
    pub async fn create_user(db: &DbConn, username: &String, email: &String, password: &String) -> String {
        let user_id: Uuid = Uuid::new_v4();
        let hashed_password: String = hash(password.as_bytes()).await;
        let new_user = users::ActiveModel {
            uuid: ActiveValue::Set(user_id),
            username: ActiveValue::Set(username.to_owned()),
            email: ActiveValue::Set(email.to_owned()),
            password_hash: ActiveValue::Set(hashed_password),
            ..Default::default()
        };
        let user_res = Users::insert(new_user).exec(db).await.unwrap();

        match user_res {
            _ => {format!("inserted")},
        }
    }

    pub async fn get_all_users(db: &DbConn, page: u64, page_size: u64) -> Result<(Vec<UserGet>, u64), DbErr> {
        let paginator = Users::find()
            .order_by_asc(users::Column::Uuid)
            // .into_json()
            .paginate(db, page_size);
        let num_pages = paginator.num_pages().await?;
        paginator.fetch_page(page - 1).await.map(|p| { 
            let mut users: Vec<UserGet> = Vec::new();
            for user in p {
                users.push(UserGet::from_model(user));
            }
            (users, num_pages)
        })
    }

    pub async fn get_one_user(db: &DbConn, user_id: Uuid) -> Result<UserGet, DbErr> {
        let user = Users::find_by_id(user_id).one(db).await;
        match user {
            Ok(user_model) => match user_model {
                Some(u) => Ok(UserGet::from_model(u)),
                None => Err(DbErr::RecordNotFound(String::from("Record not found")))
            },
            Err(err_type) => Err(err_type)
        }
    }

    pub async fn login(db: &DbConn, login: UserLogin) -> Result<TokenBodyResponse, Errors> {
        let user_got = Users::find().filter(
            Condition::any()
                .add(users::Column::Email.eq(&login.username_or_password))
                .add(users::Column::Username.eq(&login.username_or_password))
        ).one(db).await;
        match user_got {
            Ok(user) => {
                match user {
                    Some(user) => {
                        // match verify_password(login.password.as_str(), password_hash.as_bytes()) {
                        match verify_password(login.password.as_bytes(), user.password_hash.as_ref()) {
                            Ok(_) => {
                                let token = UserToken::generate_token(user.uuid);
                                return Ok(TokenBodyResponse{token: token, token_type: String::from("bearer")})
                            },
                            Err(err) => {
                                println!("login error {}", err.to_string());
                                Err(Errors::BadClientData)
                            }
                        }
                    },
                    None => return Err(Errors::NotFound)
                }
            }
            Err(_) => Err(Errors::NotFound)
        }
    }

    pub async fn get_current_user(db: &DbConn, req: HttpRequest) -> Result<UserGet, Errors> {
        if let Some(auth_header) = req.headers().get(constants::AUTHORIZATION) {
            if let Ok(auth_str) = auth_header.to_str() {
                if is_auth_header_valid(auth_header) {
                    let token = auth_str[6..auth_str.len()].trim();
                    if let Ok(token_data) = decode_token(&token.to_string()) {
                        match Query::get_one_user(db, Uuid::from_str(token_data.claims.user.as_str()).unwrap()).await {
                            Ok(login_info) => return Ok(login_info),
                            Err(_) => return Err(Errors::NotFound)
                        }
                    } else {
                        return Err(Errors::BadClientData);
                    }
                } else {
                    return Err(Errors::BadClientData);
                }
            } else {
                return Err(Errors::BadClientData);
            }
        } else {
            return Err(Errors::BadClientData);
        }
    }
}