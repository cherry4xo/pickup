use serde::{Deserialize, Serialize};
use uuid::Uuid;
use datetime::LocalDateTime;
use chrono::NaiveDate;

use crate::models::entities::{users, users::Entity as Users};

#[derive(Deserialize)]
pub struct UserCreate {
    pub username: String,
    pub email: String,
    pub password: String
}

#[derive(Serialize)]
pub struct UserGet {
    pub uuid: Uuid,
    pub username: String,
    pub email: String,
    pub password_hash: String,
    pub registration_date: NaiveDate,
    pub is_admin: bool,
    pub is_confirmed: bool
}

impl UserGet {
    pub fn new(uuid: Uuid, username: String, email: String, password_hash: String, registration_date: NaiveDate, is_admin: bool, is_confirmed: bool) -> Self {
        UserGet {
            uuid,
            username,
            email,
            password_hash,
            registration_date,
            is_admin,
            is_confirmed
        }
    }

    pub fn from_model(user: users::Model) -> Self {
        UserGet {
            uuid: user.uuid,
            username: user.username,
            email: user.email,
            password_hash: user.password_hash,
            registration_date: user.registration_date,
            is_admin: user.is_admin,
            is_confirmed: user.is_confirmed,
        }
    }
}

#[derive(Debug, Deserialize)]
pub struct Params {
    pub page: Option<u64>,
    pub page_size: Option<u64>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct UserLogin {
    pub username_or_password: String,
    pub password: String
}