use std::sync::Arc;

use axum::{
    Extension, Json,
    extract::{Path, State},
    http::StatusCode,
    response::IntoResponse,
};
use validator::Validate;

use crate::{
    AppState,
    models::{AddMeasureSchema, Measure, User},
};

pub async fn add_measure(
    State(data): State<Arc<AppState>>,
    Extension(user): Extension<User>,
    Json(body): Json<AddMeasureSchema>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    body.validate().map_err(|e| {
        (
            StatusCode::BAD_REQUEST,
            Json(serde_json::json!({
                "status": "fail",
                "message": e.to_string()
            })),
        )
    })?;

    let spot_exists = sqlx::query_scalar!(
        r#"select exists(select 1 from spots where id = $1) as "exists!""#,
        body.spot_id
    )
    .fetch_one(&data.db)
    .await
    .map_err(|e| {
        let error_response = serde_json::json!({
            "status": "fail",
            "message": format!("Error de la base de datos: {}", e),
        });
        (StatusCode::INTERNAL_SERVER_ERROR, Json(error_response))
    })?;

    if !spot_exists {
        let error_response = serde_json::json!({
            "status": "fail",
            "message": "El punto referenciado no existe",
        });
        return Err((StatusCode::NOT_FOUND, Json(error_response)));
    }

    let measure = sqlx::query_as!(
        Measure,
        r#"INSERT INTO measures (
            spot_id,
            collaborator_id,
            items_per_m2,
            weight,
            area,
            pet,
            pead,
            pebd,
            pvc,
            pp,
            ps,
            pa,
            other,
            ihr_plata,
            ibirp
        ) values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
        RETURNING *
        "#,
        body.spot_id,
        user.id,
        body.items_per_m2,
        body.weight,
        body.area,
        body.pet,
        body.pead,
        body.pebd,
        body.pvc,
        body.pp,
        body.ps,
        body.pa,
        body.other,
        body.ihr_plata,
        body.ibirp,
    )
    .fetch_one(&data.db)
    .await
    .map_err(|e| {
        let error_response = serde_json::json!({
            "status": "fail",
            "message": format!("Error de la base de datos: {}", e),
        });
        (StatusCode::INTERNAL_SERVER_ERROR, Json(error_response))
    })?;

    Ok(Json(serde_json::json!({
        "status": "success",
        "data": {
            "measure": measure
        }
    })))
}

pub async fn delete_measure(
    State(data): State<Arc<AppState>>,
    Path(measure_id): Path<uuid::Uuid>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let result = sqlx::query!("DELETE FROM measures WHERE id = $1", measure_id)
        .execute(&data.db)
        .await
        .map_err(|e| {
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({
                    "status": "error",
                    "message": format!("Error de la base de datos: {e}")
                })),
            )
        })?;

    if result.rows_affected() == 0 {
        return Err((
            StatusCode::NOT_FOUND,
            Json(serde_json::json!({
                "status": "fail",
                "message": "Medición no encontrada"
            })),
        ));
    }

    Ok((
        StatusCode::OK,
        Json(serde_json::json!({
            "status": "success",
            "message": "Medición eliminada correctamente"
        })),
    ))
}

pub async fn list_measures(
    State(data): State<Arc<AppState>>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let measures = sqlx::query_as!(Measure, "SELECT * FROM measures")
        .fetch_all(&data.db)
        .await
        .map_err(|e| {
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({
                    "status": "error",
                    "message": format!("Error de la base de datos: {e}")
                })),
            )
        })?;

    Ok(Json(serde_json::json!({
        "status": "success",
        "result": measures.len(),
        "data": {
            "measures": measures
        }
    })))
}

pub async fn get_measure(
    State(data): State<Arc<AppState>>,
    Path(measure_id): Path<uuid::Uuid>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let measure = sqlx::query_as!(
        Measure,
        r#"
        select *
        from measures
        where id = $1
        "#,
        measure_id
    )
    .fetch_optional(&data.db)
    .await
    .map_err(|e| {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(serde_json::json!({
                "status": "error",
                "message": format!("Error de la base de datos: {e}")
            })),
        )
    })?
    .ok_or_else(|| {
        (
            StatusCode::NOT_FOUND,
            Json(serde_json::json!({
                "status": "fail",
                "message": "Medición no encontrada"
            })),
        )
    })?;

    Ok(Json(serde_json::json!({
        "status": "success",
        "data": { "measure": measure }
    })))
}
