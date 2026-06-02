use std::sync::Arc;

use axum::{
    Extension, Json,
    extract::{Path, State},
    http::StatusCode,
    response::IntoResponse,
};
use password_auth::{generate_hash, verify_password};
use resend_rs::types::CreateEmailBaseOptions;
use uuid::Uuid;
use validator::Validate;

use crate::{
    AppState,
    models::{
        ChangeEmailSchema, ChangePasswordSchema, CreatePasswordSchema, PublicUser,
        RegisterCollaboratorSchema, User,
    },
    utils::sanitize_input,
};

pub async fn change_email(
    State(data): State<Arc<AppState>>,
    Extension(user): Extension<User>,
    Json(body): Json<ChangeEmailSchema>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    body.validate().map_err(|_| {
        (
            StatusCode::BAD_REQUEST,
            Json(serde_json::json!({
                "status": "fail",
                "message": "El email es inválido"
            })),
        )
    })?;

    let new_email = body.email.to_ascii_lowercase();

    let result = sqlx::query!(
        r#"
        update users
        set email = $1
        where id = $2
        "#,
        new_email,
        user.id
    )
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

    // No debería ocurrir pero no confio en nadie
    if result.rows_affected() == 0 {
        return Err((
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(serde_json::json!({
                "status": "fail",
                "message": "El usuario no existe"
            })),
        ));
    }

    Ok(Json(serde_json::json!({
        "status": "success",
        "message": "Email actualizado correctamente",
        "data": { "email": new_email }
    })))
}

pub async fn change_password(
    State(data): State<Arc<AppState>>,
    Extension(user): Extension<User>,
    Json(body): Json<ChangePasswordSchema>,
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

    if verify_password(body.old_password.clone(), &user.password).is_err() {
        return Err((
            StatusCode::BAD_REQUEST,
            Json(serde_json::json!({
                "status": "fail",
                "message": "La contraseña actual es incorrecta"
            })),
        ));
    }

    if body.old_password == body.new_password {
        return Err((
            StatusCode::CONFLICT,
            Json(serde_json::json!({
                "status": "fail",
                "message": "La nueva contraseña no puede ser igual a la anterior"
            })),
        ));
    }

    let new_hash = generate_hash(body.new_password);
    let result = sqlx::query!(
        r#"
        update users
        set password = $1
        where id = $2
        "#,
        new_hash,
        user.id
    )
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

    // De nuevo
    if result.rows_affected() == 0 {
        return Err((
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(serde_json::json!({
                "status": "error",
                "message": "El usuario no existe"
            })),
        ));
    }

    Ok(Json(serde_json::json!({
        "status": "success",
        "message": "Contraseña actualizada correctamente"
    })))
}

pub async fn create_password(
    State(data): State<Arc<AppState>>,
    Json(body): Json<CreatePasswordSchema>,
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

    let decoded_token = base62::decode(&body.token).map_err(|_| {
        (
            StatusCode::BAD_REQUEST,
            Json(serde_json::json!({
                "status": "fail",
                "message": "El token no se pudo decodificar"
            })),
        )
    })?;

    let name = sanitize_input(&body.name);
    let surname = sanitize_input(&body.surname);
    let token_hash = generate_hash(uuid::Uuid::from_u128(decoded_token));
    let password_hash = generate_hash(body.password);
    let result = sqlx::query!(
        r#"
        update users
        set password = $1, generation_token = NULL, name = $3, surname = $4
        where generation_token = $2
        "#,
        password_hash,
        token_hash,
        name,
        surname
    )
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

    // Si no cambió nada entonces no existe un usuario con ese token
    if result.rows_affected() == 0 {
        return Err((
            StatusCode::CONFLICT,
            Json(serde_json::json!({
                "status": "fail",
                "message": "Esta invitación no existe o ya fue aceptada."
            })),
        ));
    }

    // Eliminamos el token viejo, obviamente

    Ok(Json(serde_json::json!({
        "status": "success",
        "message": "Contraseña actualizada correctamente"
    })))
}

pub async fn list_collaborators(
    State(data): State<Arc<AppState>>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let users = sqlx::query_as!(User, "SELECT * FROM users ORDER BY email asc")
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
        "result": users.len(),
        "data": {
            "users": users
        }
    })))
}

pub async fn register_collaborator(
    State(data): State<Arc<AppState>>,
    Json(body): Json<RegisterCollaboratorSchema>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    match body.validate() {
        Ok(_) => (),
        Err(_) => {
            let error_response = serde_json::json!({
                "status": "fail",
                "message": "El email es inválido"
            });
            return Err((StatusCode::BAD_REQUEST, Json(error_response)));
        }
    }

    let user_exists: Option<bool> =
        sqlx::query_scalar("SELECT EXISTS(SELECT 1 FROM users WHERE email = $1)")
            .bind(body.email.to_owned().to_ascii_lowercase())
            .fetch_one(&data.db)
            .await
            .map_err(|e| {
                let error_response = serde_json::json!({
                    "status": "fail",
                    "message": format!("Error de la base de datos: {}", e),
                });
                (StatusCode::INTERNAL_SERVER_ERROR, Json(error_response))
            })?;

    if let Some(exists) = user_exists {
        if exists {
            let error_response = serde_json::json!({
                "status": "fail",
                "message": "Ese email ya se encuentra en uso",
            });
            return Err((StatusCode::CONFLICT, Json(error_response)));
        }
    }

    let password = generate_hash(Uuid::new_v4()); // Contraseña random para evitar problemas de base de datos.
    let generation_token = base62::encode(Uuid::new_v4().as_u128());
    let generation_token_hash = generate_hash(generation_token.clone());

    let user = sqlx::query_as!(
        User,
        "INSERT INTO users (email,password,generation_token) VALUES ($1, $2, $3) RETURNING *",
        body.email.to_owned().to_ascii_lowercase(),
        password,
        generation_token_hash
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

    let email = CreateEmailBaseOptions::new(
        "ContaminApp <contaminapp@example.com>",
        [body.email],
        "Invitación a colaborar en ContaminApp"
    ).with_html(format!(r#"
        <h1>Fuiste invitade a ContaminApp</h1>

        <p>Para finalizar la creación de tu cuenta, crea tu contraseña <a href="http://contaminapp.joacoslime.zapto.org/finalizar_registro?token={}">aquí</a></p>

        <p>O copia este enlace: http://contaminapp.joacoslime.zapto.org/finalizar_registro?token={}</p>
    "#, generation_token.clone(), generation_token.clone()).as_str());

    match data.resend.emails.send(email).await {
        Ok(_) => (),
        Err(e) => {
            // Revertir la creación de usuario si falla
            let _ = sqlx::query!("DELETE FROM users WHERE email = $1", user.email)
                .execute(&data.db)
                .await;

            let error_response = serde_json::json!({
                "status": "fail",
                "message": format!("Hubo un error enviando el mail: {}", e)
            });
            return Err((StatusCode::INTERNAL_SERVER_ERROR, Json(error_response)));
        }
    }

    let user_response = serde_json::json!({"status": "success","data": serde_json::json!({
        "user": user
    })});

    Ok(Json(user_response))
}

pub async fn delete_collaborator(
    State(data): State<Arc<AppState>>,
    Path(user_id): Path<uuid::Uuid>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let result = sqlx::query!(
        r#"
        delete from users
        where id = $1
        "#,
        user_id
    )
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
                "message": "Colaborador no encontrado"
            })),
        ));
    }

    Ok((
        StatusCode::OK,
        Json(serde_json::json!({
            "status": "success",
            "message": "Colaborador eliminado correctamente"
        })),
    ))
}

pub async fn get_collaborator(
    State(data): State<Arc<AppState>>,
    Path(user_id): Path<uuid::Uuid>,
) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    let user = sqlx::query_as!(
        PublicUser,
        r#"
        select id, email, name, surname
        from users
        where id = $1
        "#,
        user_id
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
                "message": "Colaborador no encontrado"
            })),
        )
    })?;

    Ok(Json(serde_json::json!({
        "status": "success",
        "data": { "user": user }
    })))
}
