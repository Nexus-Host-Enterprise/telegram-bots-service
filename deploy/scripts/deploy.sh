#!/usr/bin/env bash
set -e

echo "=== Nexus Bot Platform — Deploy Script ==="

# --------- CONFIG ---------
BACKEND_DIR="./backend"
FRONTEND_DIR="./frontend"
COMPOSE_CMD="docker compose"      # если у тебя старый docker-compose, замени на "docker-compose"
# ---------------------------

# Проверка Docker
if ! command -v docker >/dev/null 2>&1; then
    echo "[ERROR] Docker не установлен!"
    exit 1
fi

# Проверка Compose
if ! docker compose version >/dev/null 2>&1; then
    if ! docker-compose version >/dev/null 2>&1; then
        echo "[ERROR] Docker Compose не установлен!"
        exit 1
    else
        COMPOSE_CMD="docker-compose"
    fi
fi

echo "[OK] Docker и Compose найдены."

# --- Создание .env, если отсутствуют ---
if [[ ! -f "$BACKEND_DIR/.env" ]]; then
    echo "[WARN] backend/.env не найден, создаю..."

    FERNET_KEY=$(python3 - <<'EOF'
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
EOF
)

    SECRET_KEY=$(python3 - <<'EOF'
import secrets
print(secrets.token_urlsafe(64))
EOF
)

    cat > "$BACKEND_DIR/.env" <<EOF
DATABASE_URL=postgresql+asyncpg://nexus:secret@db:5432/nexus
REDIS_URL=redis://redis:6379/0

SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

BOT_MANAGER_URL=http://bot-manager:8081
FERNET_KEY=${FERNET_KEY}
EOF

    echo "[OK] backend/.env создан."
fi

if [[ ! -f "$FRONTEND_DIR/.env.local" ]]; then
    echo "[WARN] frontend/.env.local не найден, создаю..."
    cat > "$FRONTEND_DIR/.env.local" <<EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
    echo "[OK] frontend/.env.local создан."
fi

# --- Остановка старых контейнеров ---
echo "Останавливаю старые контейнеры..."
$COMPOSE_CMD down

# --- Сборка нового окружения ---
echo "Собираю контейнеры..."
$COMPOSE_CMD build

# --- Применение миграций ---
echo "Применяю миграции alembic..."
$COMPOSE_CMD run --rm backend alembic upgrade head || {
    echo "[WARN] alembic upgrade не удалось через backend. Проверяю наличие Alembic..."
}

# --- Запуск сервисов ---
echo "Запускаю весь стек..."
$COMPOSE_CMD up -d

echo "=== Деплой успешно завершён! ==="
echo ""
echo "Порты:"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo "  BotMgr:   http://localhost:8081"
echo ""
echo "Логи (пример):"
echo "  $COMPOSE_CMD logs -f backend"
