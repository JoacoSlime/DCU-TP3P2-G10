#[derive(Debug, Clone)]
pub struct Config {
    pub database_url: String,
    pub jwt_secret: String,
    pub backend_url: Option<String>,
    pub resend_key: String,
}

impl Config {
    pub fn init() -> Config {
        let database_url = std::env::var("DATABASE_URL").expect("DATABASE_URL must be set");
        let jwt_secret = std::env::var("JWT_SECRET").expect("JWT_SECRET must be set");
        let backend_url = std::env::var("BACKEND_URL").ok();
        let resend_key = std::env::var("RESEND_KEY").expect("RESEND_KEY must be set");
        Config {
            database_url,
            jwt_secret,
            backend_url,
            resend_key,
        }
    }
}
