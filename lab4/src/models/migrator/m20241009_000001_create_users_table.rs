use sea_orm_migration::prelude::*;
use chrono;

pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m20241009_000001_create_users_table"
    }
}

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.create_table(
            Table::create()
                .table(Users::Table)
                .col(
                    ColumnDef::new(Users::uuid)
                        .uuid()
                        .not_null()
                        .primary_key(),
                )
                .col(ColumnDef::new(Users::username).string().not_null())
                .col(ColumnDef::new(Users::email).string().not_null())
                .col(ColumnDef::new(Users::password_hash).string().not_null())
                .col(
                    ColumnDef::new(Users::registration_date)
                        .date()
                        .not_null()
                        .default(chrono::Utc::now().date_naive()),
                )
                .col(ColumnDef::new(Users::is_admin).boolean().not_null().default(false))
                .col(
                    ColumnDef::new(Users::is_confirmed).boolean().not_null().default(false),
                )
                .to_owned()
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .drop_table(Table::drop().table(Users::Table).to_owned())
            .await
    }
}


#[derive(Iden)]
pub enum Users {
    Table,
    uuid,
    username,
    email,
    password_hash,
    registration_date,
    is_admin,
    is_confirmed
}