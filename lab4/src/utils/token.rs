use uuid::Uuid;
use std::str::FromStr;
use sea_orm::DbErr;
use actix_web::{web, http::header::HeaderValue};
use jsonwebtoken::{DecodingKey, TokenData, Validation};
use sea_orm::*;

use crate::models::entities::{users, users::Entity as Users};
use crate::schemas::{token::{UserToken, KEY}, users::UserGet};
use crate::errors::Errors;

pub fn decode_token(token: &String) -> jsonwebtoken::errors::Result<TokenData<UserToken>> {
    jsonwebtoken::decode::<UserToken>(
        token,
        &DecodingKey::from_secret(&KEY),
        &Validation::default()
    )
}

pub fn is_auth_header_valid(authen_header: &HeaderValue) -> bool {
    if let Ok(authen_str) = authen_header.to_str() {
        return authen_str.starts_with("bearer") || authen_str.starts_with("Bearer");
    }

    return false;
}

pub async fn get_current_user(db: &DbConn, user_token: &String) -> Result<UserGet, Errors> {
    match decode_token(user_token) {
        Ok(token_data) => {
            if token_data.claims.exp > chrono::Utc::now().timestamp_nanos_opt().unwrap() {
                return Err(Errors::Unauthorized)
            }
            let user_id = Uuid::from_str(token_data.claims.user.as_str()).unwrap();
            let user = Users::find_by_id(user_id).one(db).await;
            match user {
                Ok(user_model) => match user_model {
                    Some(u) => Ok(UserGet::from_model(u)),
                    None => Err(Errors::NotFound)
                },
                Err(_) => Err(Errors::NotFound)
            }
        },
        Err(_) => Err(Errors::BadClientData)
    }
}