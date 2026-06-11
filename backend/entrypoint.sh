#!/usr/bin/env sh
set -eu

if [ -z "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL no existe" >&2
  exit 1
fi
if [ -z "${JWT_SECRET:-}" ]; then
  echo "JWT_SECRET no existe" >&2
  exit 1
fi
if [ -z "${RESEND_KEY:-}" ]; then
  echo "RESEND_KEY no existe" >&2
  exit 1
fi

until pg_isready -d "${DATABASE_URL}" >/dev/null 2>&1; do
  echo "Esperando a postgres..."
  sleep 1
done

# ejecutar migraciones con sqlx (usa DATABASE_URL)
echo "Ejecutando migraciones..."
sqlx migrate run

echo "Iniciando backend en :3000"
exec /usr/local/bin/contaminapp_backend
