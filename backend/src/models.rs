use serde::{Deserialize, Serialize};
use sqlx::prelude::FromRow;
use validator::Validate;

use crate::utils::{validate_password, validate_positive_decimal};

#[derive(Debug, FromRow, Serialize, Deserialize, Clone)]
pub struct User {
    pub id: uuid::Uuid,
    pub email: String,
    #[serde(skip_serializing)]
    pub password: String,
    #[serde(skip_serializing, rename = "generationToken")]
    pub generation_token: Option<String>,
    pub name: Option<String>,
    pub surname: Option<String>,
}

#[derive(Debug, FromRow, Serialize, Deserialize, Clone)]
pub struct PublicUser {
    pub id: uuid::Uuid,
    pub email: String,
    pub name: Option<String>,
    pub surname: Option<String>,
}

#[derive(Debug, FromRow, Serialize, Deserialize, Clone)]
pub struct Spot {
    pub id: uuid::Uuid,
    pub title: String,
    pub latitude: rust_decimal::Decimal,
    pub longitude: rust_decimal::Decimal,
}

#[derive(Debug, FromRow, Serialize, Deserialize, Clone)]
pub struct SpotWithMeasure {
    pub spot_id: uuid::Uuid,
    pub measure_id: uuid::Uuid,
    pub title: String,
    pub latitude: rust_decimal::Decimal,
    pub longitude: rust_decimal::Decimal,
    pub collaborator_id: uuid::Uuid,
    pub created_at: time::OffsetDateTime,
    pub items_per_m2: rust_decimal::Decimal,
    pub weight: rust_decimal::Decimal,
    pub area: rust_decimal::Decimal,
    pub pet: i32,
    pub pead: i32,
    pub pebd: i32,
    pub pvc: i32,
    pub pp: i32,
    pub ps: i32,
    pub pa: i32,
    pub other: i32,
    pub ihr_plata: rust_decimal::Decimal,
    pub ibirp: rust_decimal::Decimal,
}

#[derive(Debug, FromRow, Serialize, Deserialize, Clone)]
pub struct Measure {
    pub id: uuid::Uuid,
    pub spot_id: uuid::Uuid,
    pub collaborator_id: uuid::Uuid,
    pub created_at: time::OffsetDateTime,
    pub items_per_m2: rust_decimal::Decimal,
    pub weight: rust_decimal::Decimal,
    pub area: rust_decimal::Decimal,
    pub pet: i32,
    pub pead: i32,
    pub pebd: i32,
    pub pvc: i32,
    pub pp: i32,
    pub ps: i32,
    pub pa: i32,
    pub other: i32,
    pub ihr_plata: rust_decimal::Decimal,
    pub ibirp: rust_decimal::Decimal,
}

// Payloads

#[derive(Debug, Serialize)]
pub struct ErrorResponse {
    pub status: &'static str,
    pub message: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct TokenClaims {
    pub sub: String,
    pub iat: usize,
    pub exp: usize,
}

// Payload schemas

#[derive(Debug, Deserialize, Validate)]
pub struct RegisterCollaboratorSchema {
    #[validate(email)]
    pub email: String,
}

#[derive(Debug, Deserialize, Validate)]
pub struct LoginUserSchema {
    #[validate(email)]
    pub email: String,
    pub password: String,
}

#[derive(Debug, Deserialize, Validate)]
pub struct ChangeEmailSchema {
    #[validate(email)]
    pub email: String,
}

#[derive(Debug, Deserialize, Validate)]
pub struct ChangePasswordSchema {
    pub old_password: String,
    #[validate(custom(function = "validate_password"))]
    pub new_password: String,
}

#[derive(Debug, Deserialize, Validate)]
pub struct CreatePasswordSchema {
    pub token: String,
    #[validate(length(min = 1))]
    pub name: String,
    #[validate(length(min = 1))]
    pub surname: String,
    #[validate(custom(function = "validate_password"))]
    pub password: String,
}

#[derive(Debug, Deserialize, Validate)]
pub struct AddSpotSchema {
    #[validate(length(min = 1, max = 255))]
    pub title: String,
    pub latitude: rust_decimal::Decimal,
    pub longitude: rust_decimal::Decimal,
    #[validate(custom(function = "validate_positive_decimal"))]
    pub items_per_m2: rust_decimal::Decimal,
    #[validate(custom(function = "validate_positive_decimal"))]
    pub weight: rust_decimal::Decimal,
    #[validate(custom(function = "validate_positive_decimal"))]
    pub area: rust_decimal::Decimal,
    pub pet: i32,
    pub pead: i32,
    pub pebd: i32,
    pub pvc: i32,
    pub pp: i32,
    pub ps: i32,
    pub pa: i32,
    pub other: i32,
    #[validate(custom(function = "validate_positive_decimal"))]
    pub ihr_plata: rust_decimal::Decimal,
    #[validate(custom(function = "validate_positive_decimal"))]
    pub ibirp: rust_decimal::Decimal,
}

#[derive(Debug, Deserialize, Validate)]
pub struct AddMeasureSchema {
    pub spot_id: uuid::Uuid,
    #[validate(custom(function = "validate_positive_decimal"))]
    pub items_per_m2: rust_decimal::Decimal,
    #[validate(custom(function = "validate_positive_decimal"))]
    pub weight: rust_decimal::Decimal,
    #[validate(custom(function = "validate_positive_decimal"))]
    pub area: rust_decimal::Decimal,
    pub pet: i32,
    pub pead: i32,
    pub pebd: i32,
    pub pvc: i32,
    pub pp: i32,
    pub ps: i32,
    pub pa: i32,
    pub other: i32,
    #[validate(custom(function = "validate_positive_decimal"))]
    pub ihr_plata: rust_decimal::Decimal,
    #[validate(custom(function = "validate_positive_decimal"))]
    pub ibirp: rust_decimal::Decimal,
}
