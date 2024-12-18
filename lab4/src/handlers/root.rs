use actix_web::{get, http::StatusCode, post, web, App, HttpRequest, HttpResponse, Responder};


#[get("/")]
async fn index() -> impl Responder {
    HttpResponse::Ok().body("Hello, world!")
}

pub async fn page_not_found() -> impl Responder {
    HttpResponse::NotFound().body("Error 404. Page not found.")
}