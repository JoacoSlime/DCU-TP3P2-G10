use std::error::Error;

use ammonia::clean;
use sqlx::PgPool;
use uuid::Uuid;
use validator::ValidationError;

pub fn sanitize_input(input: &str) -> String {
    clean(input).to_string()
}

pub fn validate_password(password: &str) -> Result<(), ValidationError> {
    if password.chars().count() < 8 {
        return Err(ValidationError::new("password_too_short")
            .with_message("La nueva contraseña debe tener al menos 8 caracteres".into()));
    }

    let (mut has_upper, mut has_lower, mut has_digit) = (false, false, false);

    for ch in password.chars() {
        if !has_upper && ch.is_uppercase() {
            has_upper = true;
        }
        if !has_lower && ch.is_lowercase() {
            has_lower = true;
        }
        if !has_digit && ch.is_ascii_digit() {
            has_digit = true;
        }

        if has_upper && has_lower && has_digit {
            return Ok(());
        }
    }

    let mut lacks: Vec<&'static str> = Vec::new();

    if !has_digit {
        lacks.push("un número");
    }
    if !has_lower {
        lacks.push("una letra minúscula");
    }
    if !has_upper {
        lacks.push("una letra mayúscula");
    }

    let msg = match lacks.len() {
        0 => return Ok(()), // No debería ocurrir
        1 => format!("Falta al menos {}", lacks[0]),
        2 => format!("Falta al menos {} y {}", lacks[0], lacks[1]),
        _ => {
            let last = lacks[lacks.len() - 1];
            let head = &lacks[..lacks.len() - 1];
            format!("Falta al menos {} y {}", head.join(", "), last)
        }
    };

    Err(ValidationError::new("character_conditions_not_met").with_message(msg.into()))
}

pub fn validate_positive_decimal(decimal: &rust_decimal::Decimal) -> Result<(), ValidationError> {
    if decimal.is_sign_positive() || decimal.is_zero() {
        Ok(())
    } else {
        Err(ValidationError::new("negative_decimal")
            .with_message("El valor decimal no puede ser negativo".into()))
    }
}

pub async fn has_admin_user(pool: &PgPool) -> Result<bool, Box<dyn Error>> {
    // Returns true if at least one user belongs to the "administrators" group.
    let exists: (bool,) = sqlx::query_as(
        r#"
        SELECT EXISTS(
            SELECT 1
            FROM users u
            JOIN users_groups ug ON u.id = ug.user_id
            JOIN groups g ON ug.group_id = g.id
            WHERE g.name = 'administrators'
        ) ;
        "#,
    )
    .fetch_one(pool)
    .await?;
    Ok(exists.0)
}

pub async fn add_admin(db: &PgPool, user_id: Uuid) -> Result<(), Box<dyn Error>> {
    // get administrators group id
    let admin_group_id: Option<Uuid> = sqlx::query_scalar!(
        r#"
        select id::uuid
        from groups
        where name = 'administrators'
        limit 1
        "#
    )
    .fetch_optional(db)
    .await?;

    let admin_group_id = admin_group_id
        .ok_or_else(|| Box::new(std::io::Error::other("administrators group not found")))?;

    // get collaborators group id
    let collab_group_id: Option<Uuid> = sqlx::query_scalar!(
        r#"
        select id::uuid
        from groups
        where name = 'collaborators'
        limit 1
        "#
    )
    .fetch_optional(db)
    .await?;

    let collab_group_id = collab_group_id
        .ok_or_else(|| Box::new(std::io::Error::other("collaborators group not found")))?;

    // ensure user exists
    let user_exists: bool = sqlx::query_scalar!(
        r#"
        select exists (
            select 1 from users where id = $1
        ) as "exists!"
        "#,
        user_id
    )
    .fetch_one(db)
    .await?;

    if !user_exists {
        return Err(Box::new(std::io::Error::other("target user not found")));
    }

    // add to administrators (idempotent)
    sqlx::query!(
        r#"
        insert into users_groups (user_id, group_id)
        values ($1, $2)
        on conflict do nothing
        "#,
        user_id,
        admin_group_id
    )
    .execute(db)
    .await?;

    // add to collaborators (idempotent)
    sqlx::query!(
        r#"
        insert into users_groups (user_id, group_id)
        values ($1, $2)
        on conflict do nothing
        "#,
        user_id,
        collab_group_id
    )
    .execute(db)
    .await?;

    Ok(())
}
