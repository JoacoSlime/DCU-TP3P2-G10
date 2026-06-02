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
    models::{AddSpotSchema, Measure, Spot, SpotWithMeasure, User},
    utils::sanitize_input,
};

pub async fn add_spot(
    State(data): State<Arc<AppState>>,
    Extension(user): Extension<User>,
    Json(body): Json<AddSpotSchema>,
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
        "SELECT EXISTS(SELECT 1 FROM spots WHERE title = $1)",
        body.title.to_owned()
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

    if let Some(exists) = spot_exists {
        if exists {
            let error_response = serde_json::json!({
                "status": "fail",
                "message": "Ya existe un punto con ese título",
            });
            return Err((StatusCode::CONFLICT, Json(error_response)));
        }
    }

    let title = sanitize_input(&body.title);
    let spot = sqlx::query_as!(
        Spot,
        "INSERT INTO spots (title, latitude, longitude) VALUES ($1, $2, $3) RETURNING *",
        title,
        body.latitude,
        body.longitude
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
        spot.id,
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
            "spot": spot,
            "measure": measure
        }
    })))
}

pub async fn delete_spot(
    State(data): State<Arc<AppState>>,
    Path(spot_id): Path<uuid::Uuid>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let result = sqlx::query!("DELETE FROM spots WHERE id = $1", spot_id)
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
                "message": "Punto no encontrado"
            })),
        ));
    }

    Ok((
        StatusCode::OK,
        Json(serde_json::json!({
            "status": "success",
            "message": "Punto eliminado correctamente"
        })),
    ))
}

pub async fn list_spots(
    State(data): State<Arc<AppState>>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let spots = sqlx::query_as!(
        SpotWithMeasure,
        r#"
        select
            s.id as "spot_id!",
            m.id as "measure_id!",
            s.title,
            s.latitude,
            s.longitude,
            m.collaborator_id,
            m.created_at,
            m.items_per_m2,
            m.weight,
            m.area,
            m.pet,
            m.pead,
            m.pebd,
            m.pvc,
            m.pp,
            m.ps,
            m.pa,
            m.other,
            m.ihr_plata,
            m.ibirp
        from spots s
        join lateral (
            select *
            from measures
            where spot_id = s.id
            order by created_at desc
            limit 1
        ) m on true
        order by s.title asc
        "#
    )
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
        "result": spots.len(),
        "data": {
            "spots": spots
        }
    })))
}

pub async fn get_spot(
    State(data): State<Arc<AppState>>,
    Path(spot_id): Path<uuid::Uuid>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let spot = sqlx::query_as!(
        SpotWithMeasure,
        r#"
        select
            s.id as "spot_id!",
            m.id as "measure_id!",
            s.title,
            s.latitude,
            s.longitude,
            m.collaborator_id,
            m.created_at,
            m.items_per_m2,
            m.weight,
            m.area,
            m.pet,
            m.pead,
            m.pebd,
            m.pvc,
            m.pp,
            m.ps,
            m.pa,
            m.other,
            m.ihr_plata,
            m.ibirp
        from spots s
        join lateral (
            select *
            from measures
            where spot_id = s.id
            order by created_at desc
            limit 1
        ) m on true
        where s.id = $1
        "#,
        spot_id
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
                "message": "Punto no encontrado"
            })),
        )
    })?;

    Ok(Json(serde_json::json!({
        "status": "success",
        "data": { "spot": spot }
    })))
}

pub async fn get_measures(
    Path(spot_id): Path<uuid::Uuid>,
    State(data): State<Arc<AppState>>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let measures = sqlx::query_as!(
        Measure,
        "SELECT * FROM measures WHERE spot_id = $1",
        spot_id
    )
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
