#!/usr/bin/env bash
set -euo pipefail

COMPOSE="docker compose -f docker-compose.prod.yml"

echo "=== Nexus Bot Platform — Production deploy ==="

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not installed"; exit 1
fi

# Pull latest images for services that are published (optional)
# $COMPOSE pull || true

# Build local images (backend/frontend)
$COMPOSE build --pull

# Create .env in backend and other places if needed (we assume done)
# Run migrations: run alembic inside backend build
$COMPOSE run --rm backend alembic upgrade head

# Start services in detached mode
$COMPOSE up -d

echo "Services starting. Show status:"
$COMPOSE ps

echo "Prometheus: http://<SERVER_IP>:9090"
echo "Grafana: http://<SERVER_IP>:3001 (admin:${GRAFANA_ADMIN_PASSWORD:-admin})"
echo "SWAG (HTTPS): https://${DOMAIN}"
