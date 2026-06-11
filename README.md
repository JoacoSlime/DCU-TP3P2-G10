# ContaminApp - Grupo 10

## Corriendo el Backend

> Nota: Puede utilizarse el backend default si fuera necesario.

Desde la carpeta `backend` crear un archivo `.env` basado en `.env.example`:

- Ejecutar con `docker compose up --build`

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

- Instalar con `bun run build`
- Compilar estáticos con `bun cap sync android`
- Abrir en android studio con `bun cap open android`
- En Android Studio: `Build → Generate Signed Bundle/APK` y Compilar APK

## Variables de ambiente

### Backend

- DATABASE_URL: Indica al backend la dirección de postgres.
- RESEND_KEY: Key de la api de Resend para el envio de emails.
- JWT_SECRET: Secreto JWT utilizado para la autentificación con jsonwebtokens.
- BACKEND_URL (opcional): URL del backend, utilizado por CORS.

### Frontend

- API_URL: URL de la API del backend.
