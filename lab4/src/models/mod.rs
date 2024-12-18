use sea_orm::{Database, DbErr, ConnectionTrait, DbBackend, Statement};
mod migrator;
pub mod entities;
use migrator::Migrator;
use sea_orm_migration::prelude::*;

pub const DATABASE_URL: &str = "postgres://postgres:256128@0.0.0.0:5435";
pub const DATABASE_NAME: &str = "users";

pub async fn run() -> Result<(), DbErr> {
    let db = Database::connect(DATABASE_URL).await?;

    let db = &match db.get_database_backend() {
        DbBackend::Postgres => {
            db.execute(Statement::from_string(
                db.get_database_backend(),
                format!("DROP DATABASE IF EXISTS \"{}\";", DATABASE_NAME),
            ))
            .await?;
            db.execute(Statement::from_string(
                db.get_database_backend(),
                format!("CREATE DATABASE \"{}\";", DATABASE_NAME),
            ))
            .await?;

            let url = format!("{}/{}", DATABASE_URL, DATABASE_NAME);
            Database::connect(&url).await?
        },
        DbBackend::MySql => {
            db.execute(Statement::from_string(
               db.get_database_backend(),
               format!("CREATE DATABASE IF NOT EXISTS `{}`;", DATABASE_NAME),
           ))
           .await?;

           let url = format!("{}/{}", DATABASE_URL, DATABASE_NAME);
           Database::connect(&url).await?
        },
        DbBackend::Sqlite => db,
    };

    let schema_manager = SchemaManager::new(db);
    Migrator::refresh(db).await?;
    assert!(schema_manager.has_table("users").await?);

    Ok(())
}
