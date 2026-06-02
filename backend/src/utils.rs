use ammonia::clean;
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
