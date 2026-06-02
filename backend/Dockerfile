# syntax=docker/dockerfile:1

FROM rust:1.96 AS builder
WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    pkg-config \
    libssl-dev \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Cache de dependencias: ahora Cargo.toml/lock están en el mismo dir (backend/)
COPY Cargo.toml Cargo.lock ./
RUN mkdir -p src \
  && printf "fn main() {}\n" > src/main.rs \
  && cargo build --release \
  && rm -rf src

# Copiamos el código real del backend (todo el directorio backend/)
COPY . .

RUN cargo build --release --locked

RUN cargo install sqlx-cli --locked --no-default-features --features postgres --root /usr/local

FROM debian:trixie-slim AS runtime
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl3 \
    postgresql-client\
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/target/release/contaminapp_backend /usr/local/bin/contaminapp_backend
COPY --from=builder /usr/local/bin/sqlx /usr/local/bin/sqlx
COPY migrations ./migrations
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV RUST_LOG=info
EXPOSE 3000
ENTRYPOINT ["/entrypoint.sh"]
