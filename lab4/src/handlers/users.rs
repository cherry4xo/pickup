use std::fmt::format;
use std::str::FromStr;
use actix_web::{get, http::StatusCode, post, web, HttpResponse, HttpRequest, Responder, Result, Error};
use sea_orm::*;
use serde_json::json;
use uuid::{uuid, Uuid};

use crate::schemas::users;
use crate::service::users::Query;
use super::AppState;
use crate::errors::Errors;

#[post("/")]
async fn create_user(data: web::Json<users::UserCreate>, state: web::Data<AppState>) -> impl Responder {
    let conn = &state.conn;
    let username: String = data.username.clone();
    let email: String = data.email.clone();
    let password: String = data.password.clone();

    Query::create_user(conn , &username, &email, &password).await;

    format!("created")
}

#[get("/")]
async fn get_all_users(req: HttpRequest, state: web::Data<AppState>) -> web::Json<serde_json::Value> {
    let conn = &state.conn;
    let params = web::Query::<users::Params>::from_query(req.query_string()).unwrap();
    let page = params.page.unwrap_or(1);
    let page_size = params.page_size.unwrap_or(5);
    let (users, num_pages) = Query::get_all_users(conn, page, page_size)
        .await
        .expect("Cannot find users in page");
    web::Json(json!({
        "users": users,
        "num_pages": num_pages
    }))
}

#[get("/{id}")]
async fn get_user(path: web::Path<String>, state: web::Data<AppState>) -> Result<HttpResponse, Error> {
    let conn = &state.conn;
    let got_id = Uuid::from_str(path.into_inner().as_str());
    match got_id {
        Ok(id) => {
            let user = Query::get_one_user(conn, id).await;
            match user {
                Ok(user) => Ok(HttpResponse::Ok().json(user)),
                Err(e) => {
                    println!("{:?}", e);
                    Ok(HttpResponse::NotFound().json("User not found"))
                }
            }
        },
        Err(_) => Ok(HttpResponse::BadRequest().json("Invalid UUID"))
    }
}

#[post("/login")]
async fn login(data: web::Json<users::UserLogin>, state: web::Data<AppState>) -> Result<HttpResponse, Errors> {
    let conn = &state.conn;

    match Query::login(conn, data.into_inner()).await {
        Ok(token) => Ok(HttpResponse::Ok().json(token)),
        Err(_) => Err(Errors::BadClientData)
    }
}

#[get("/me")]
async fn get_user_me(req: HttpRequest, state: web::Data<AppState>) -> Result<HttpResponse, Errors> {
    let conn = &state.conn;
    match Query::get_current_user(conn, req).await {
        Ok(user) => Ok(HttpResponse::Ok().json(user)),
        Err(e) => Err(Errors::NotFound)
    }
}