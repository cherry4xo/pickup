use sea_orm::DatabaseConnection;

pub mod root;
pub mod users;

#[derive(Debug, Clone)]
pub struct AppState {
    pub conn: DatabaseConnection,
}