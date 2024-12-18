use sea_orm::entity::prelude::*;
use std::cmp::{Eq, PartialEq};
use uuid::Uuid;
use chrono::NaiveDate;

#[derive(Clone, Debug, PartialEq, Eq, DeriveEntityModel)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub uuid: Uuid,
    pub username: String,
    pub email: String,
    pub password_hash: String,
    pub registration_date: NaiveDate,
    pub is_admin: bool,
    pub is_confirmed: bool
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}