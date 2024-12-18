use actix_web::dev::{Service, ServiceRequest, ServiceResponse, Transform};
use actix_web::http::{
    header::{HeaderName, HeaderValue},
    Method,
};
use actix_web::web::Data;
use actix_web::Error;
use actix_web::HttpResponse;
use futures::future::{ok, LocalBoxFuture, Ready};
use log::{error, info};

pub struct Authentication;