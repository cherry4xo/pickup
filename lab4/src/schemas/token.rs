use chrono::Utc;
use jsonwebtoken::{EncodingKey, Header};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::models::entities::{users, users::Entity as Users};

pub static KEY: [u8; 63] = *include_bytes!("../secret.key");
static ONE_WEEK: i64 = 60 * 60 * 24 * 7;

#[derive(Serialize, Deserialize)]
pub struct UserToken {
    pub iat: i64,
    pub exp: i64,
    pub user: String
}

#[derive(Serialize, Deserialize)]
pub struct TokenBodyResponse {
    pub token: String,
    pub token_type: String
}

impl UserToken {
    pub fn generate_token(user_id: Uuid) -> String {
        let max_age: i64 = ONE_WEEK;

        let now = Utc::now().timestamp_nanos_opt().unwrap();
        let payload = UserToken {
            iat: now,
            exp: now + max_age,
            user: user_id.to_string()
        };

        jsonwebtoken::encode(
            &Header::default(),
            &payload,
            &EncodingKey::from_secret(&KEY)
        )
        .unwrap()
    }
}