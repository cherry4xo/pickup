use actix_web::{
    error, get,
    http::{header::ContentType, StatusCode},
    App, HttpResponse,
};
use base64::display;
use derive_more::{Display, Error};

#[derive(Debug, Display, Error)]
pub enum Errors {
    #[display(fmt="internal error")]
    InternalError,

    #[display(fmt="bad request")]
    BadClientData,

    #[display(fmt="timeout")]
    Timeout,

    #[display(fmt="not found")]
    NotFound,

    #[display(fmt="unauthorized")]
    Unauthorized,

    #[display(fmt="forbidden")]
    Forbidden,
}

impl error::ResponseError for Errors {
    fn error_response(&self) -> HttpResponse {
        HttpResponse::build(self.status_code())
            .insert_header(ContentType::html())
            .body(self.to_string())
    }

    fn status_code(&self) -> StatusCode {
        match *self {
            Errors::InternalError => StatusCode::INTERNAL_SERVER_ERROR,
            Errors::BadClientData => StatusCode::BAD_REQUEST,
            Errors::Timeout => StatusCode::GATEWAY_TIMEOUT,
            Errors::NotFound => StatusCode::NOT_FOUND,
            Errors::Unauthorized => StatusCode::UNAUTHORIZED,
            Errors::Forbidden => StatusCode::FORBIDDEN,
        }
    }
}