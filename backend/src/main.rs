mod api;
mod auth;
mod config;
mod models;
mod route;
mod utils;

use std::sync::Arc;

use axum::http::{
    HeaderValue, Method,
    header::{ACCEPT, AUTHORIZATION, CONTENT_TYPE},
};
use password_auth::generate_hash;
use resend_rs::Resend;
use sqlx::{Pool, Postgres, postgres::PgPoolOptions};
use tower_http::cors::CorsLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use crate::{
    config::Config,
    route::create_router,
    utils::{add_admin, has_admin_user},
};

pub struct AppState {
    db: Pool<Postgres>,
    env: Config,
    resend: Resend,
}

#[tokio::main]
async fn main() {
    println!("Cargando variables de ambiente y configuración...");
    dotenv::dotenv().ok();
    let config = Config::init();

    println!("Conectando con la base de datos...");
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&config.database_url)
        .await
        .expect("Error conectando con la base de datos");

    // Esto habría que moverlo... pero-
    let admin_exists = has_admin_user(&pool)
        .await
        .expect("Error al conectar a la base de datos");
    if !admin_exists {
        let user_id = sqlx::query!(
            r#"
            INSERT INTO users (email,password) VALUES ($1, $2) RETURNING id
            "#,
            "admin@admin.com",
            generate_hash("admin"),
        )
        .fetch_one(&pool)
        .await
        .expect("Error al crear el admin")
        .id;
        add_admin(&pool, user_id)
            .await
            .expect("Error al dar permisos de administrador al usuario admin");
    }

    println!("Construyendo aplicación...");
    let mut cors = CorsLayer::new()
        .allow_origin("http://localhost:3000".parse::<HeaderValue>().unwrap())
        .allow_methods([Method::GET, Method::POST, Method::PATCH, Method::DELETE])
        .allow_credentials(true)
        .allow_headers([AUTHORIZATION, ACCEPT, CONTENT_TYPE]);

    if let Some(url) = config.clone().backend_url {
        cors = cors.allow_origin(url.parse::<HeaderValue>().unwrap())
    }

    let resend = Resend::new(&config.resend_key.clone());

    // initialize tracing
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| format!("{}=debug", env!("CARGO_CRATE_NAME")).into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    // build our application with a route
    let app = create_router(Arc::new(AppState {
        db: pool.clone(),
        env: config.clone(),
        resend: resend.clone(),
    }))
    .layer(cors);

    println!("Server iniciado, escuchando en 0.0.0.0:3000");

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    match axum::serve(listener, app).await {
        Ok(_) => println!("Server detenido."),
        Err(e) => panic!("Hubo un error en el servidor: {}", e),
    }
}
