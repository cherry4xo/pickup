use futures::executor::block_on;
use actix_web::{get, post, web, App, HttpRequest, HttpResponse, HttpServer, Responder};
use sea_orm::{Database, DatabaseConnection};

pub mod handlers;
pub mod models;
pub mod schemas;
pub mod service;
pub mod utils;
pub mod middleware;
pub mod errors;
pub mod constants;
use handlers::{root, users, AppState};
use models::{DATABASE_URL, DATABASE_NAME};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    std::env::set_var("RUST_LOG", "info");
    std::env::set_var("RUST_BACKTRACE", "1");

    // if let Err(err) = block_on(models::run()) {
    //     panic!("{}", err);
    // }
    let db_url = format!("{DATABASE_URL}/{DATABASE_NAME}");
    let conn = Database::connect(db_url).await.unwrap();
    let state = AppState {conn: conn};

    println!("Created DB");

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(state.clone()))
            .service(root::index)
            .service(
                web::scope("/users")
                    .service(users::create_user)
                    .service(users::get_all_users)
                    .service(users::get_user)
                    .service(users::login)
                    .service(users::get_user_me)
            )
            .default_service(
                web::route().to(root::page_not_found)
            )
    })
    .bind(("127.0.0.1", 8083))?
    .run()
    .await
}
