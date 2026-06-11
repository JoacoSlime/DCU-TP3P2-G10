use std::sync::Arc;

use axum::{
    Json, Router, middleware,
    response::IntoResponse,
    routing::{delete, get, post},
};

use crate::{
    AppState,
    api::{
        auth::{login, logout, me},
        collaborators::{
            change_email, change_password, create_password, delete_collaborator, get_collaborator,
            list_collaborators, register_collaborator,
        },
        measures::{add_measure, delete_measure, get_measure, list_measures},
        sposts::{add_spot, delete_spot, get_measures, get_spot, list_spots},
    },
    auth::{auth, require_permission},
};

pub fn create_router(app_state: Arc<AppState>) -> Router {
    Router::new()
        // Unauthenticated routes
        .route("/api/healthcheck", get(health_checker))
        .route("/api/auth/me", get(me))
        .route("/api/auth/login", post(login))
        .route("/api/collaborators/create_password", post(create_password))
        .route("/api/collaborators/get/:user_id", get(get_collaborator))
        .route("/api/measures/get/:measure_id", get(get_measure))
        .route("/api/measures/list", get(list_measures))
        .route("/api/spots/get/:spot_id", get(get_spot))
        .route("/api/spots/list", get(list_spots))
        .route("/api/spots/measures/:spot_id", get(get_measures))
        // Collaborator routes
        .route(
            "/api/auth/logout",
            get(logout).route_layer(middleware::from_fn_with_state(app_state.clone(), auth)),
        )
        .route(
            "/api/collaborators/change_email",
            post(change_email).route_layer(middleware::from_fn_with_state(app_state.clone(), auth)),
        )
        .route(
            "/api/collaborators/change_password",
            post(change_password)
                .route_layer(middleware::from_fn_with_state(app_state.clone(), auth)),
        )
        .route(
            "/api/measures/add",
            post(add_measure)
                .route_layer(middleware::from_fn_with_state(
                    app_state.clone(),
                    |state, req, next| require_permission(state, req, next, "measures.add"),
                ))
                .route_layer(middleware::from_fn_with_state(app_state.clone(), auth)),
        )
        .route(
            "/api/spots/add",
            post(add_spot)
                .route_layer(middleware::from_fn_with_state(
                    app_state.clone(),
                    |state, req, next| require_permission(state, req, next, "spots.add"),
                ))
                .route_layer(middleware::from_fn_with_state(app_state.clone(), auth)),
        )
        // Administrator routes
        .route(
            "/api/collaborators/register",
            post(register_collaborator)
                .route_layer(middleware::from_fn_with_state(
                    app_state.clone(),
                    |state, req, next| require_permission(state, req, next, "collaborators.add"),
                ))
                .route_layer(middleware::from_fn_with_state(app_state.clone(), auth)),
        )
        .route(
            "/api/collaborators/list",
            get(list_collaborators)
                .route_layer(middleware::from_fn_with_state(
                    app_state.clone(),
                    |state, req, next| require_permission(state, req, next, "collaborators.list"),
                ))
                .route_layer(middleware::from_fn_with_state(app_state.clone(), auth)),
        )
        .route(
            "/api/collaborators/delete/:user_id",
            delete(delete_collaborator)
                .route_layer(middleware::from_fn_with_state(
                    app_state.clone(),
                    |state, req, next| require_permission(state, req, next, "collaborators.delete"),
                ))
                .route_layer(middleware::from_fn_with_state(app_state.clone(), auth)),
        )
        .route(
            "/api/measures/delete/:measure_id",
            delete(delete_measure)
                .route_layer(middleware::from_fn_with_state(
                    app_state.clone(),
                    |state, req, next| require_permission(state, req, next, "measures.delete"),
                ))
                .route_layer(middleware::from_fn_with_state(app_state.clone(), auth)),
        )
        .route(
            "/api/spots/delete/:spot_id",
            delete(delete_spot)
                .route_layer(middleware::from_fn_with_state(
                    app_state.clone(),
                    |state, req, next| require_permission(state, req, next, "spots.delete"),
                ))
                .route_layer(middleware::from_fn_with_state(app_state.clone(), auth)),
        )
        .with_state(app_state)
}

async fn health_checker() -> impl IntoResponse {
    const MESSAGE: &str = "ContaminApp - Grupo10";

    let json_response = serde_json::json!({
        "status": "success",
        "message": MESSAGE
    });

    Json(json_response)
}
