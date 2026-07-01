# ContaminApp - Grupo 10

## Corriendo el Backend

> Nota: Puede utilizarse el backend default si fuera necesario.

Desde la carpeta `backend` crear un archivo `.env` basado en `.env.example`:

- Iniciar backend con `docker compose up`

Primer inicio:

- `docker compose exec backend flask reset-db`
- `docker compose exec backend flask seed-db`

## Corriendo el Frontend

### Navegador

Desde la carpeta `frontend`:

- Construir el Dockerfile con `docker build -t contaminapp .`
- Iniciar el frontend con `docker run -p 8080:80 contaminapp`

### Android

> Nota: Las instrucciones usan `bun` sin embargo puede usarse `npm` u otros.

Prerrequisitos:
- Android SDK 36
- Java JDK 21
- Android Studio

Desde la carpeta `frontend`:

- Compilar estáticos con `bun run build`
- Sincronizar configuración de Android con `bun cap sync android`
- Abrir en android studio con `bun cap open android`
- En Android Studio: `Build → Generate Signed Bundle/APK` y Compilar APK

## Variables de ambiente

### Backend

- `POSTGRES_PASSWORD`: Contraseña utilizada por Postres y Flask para conectarse.
- `SMTP_HOST`: Dirección del servidor SMTP (Con mailtrap `live.smtp.mailtrap.io`)
- `SMTP_PORT`: Puerto del servidor SMTP (Con mailtrap `587`)
- `SMTP_LOGIN`: Nombre de usuario del servidor SMTP (Con mailtrap `api`)
- `SMTP_PASSWORD`: Contraseña del servidor SMTP (Con mailtrap la API KEY)
- `JWT_SECRET`: Secreto JWT utilizado para la autentificación con JWT.
- `FLASK_SECRET_KEY`: Utilizado por Flask para la generación de sesiones, CSRF, etc.
- `URL_BASE_PUBLIC_APP` (opcional): URL del backend, utilizado por CORS.

### Frontend

- API_URL: URL de la API del backend.
