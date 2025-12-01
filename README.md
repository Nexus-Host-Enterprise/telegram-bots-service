<div align="center">
  <h1>Nexus Bot Platform</h1>
  <h3>Многофункциональная платформа для создания, управления и масштабирования Telegram-ботов</h3>

  <!-- Badges -->
  <p>
    <!-- License --><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
    <!-- Docker --><img src="https://img.shields.io/badge/Docker-ready-blue?style=for-the-badge" />
    <!-- FastAPI --><img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge" />
    <!-- NextJS --><img src="https://img.shields.io/badge/Frontend-Next.js-000000?style=for-the-badge" />
    <!-- Python --><img src="https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge" />
  </p>
</div>

---

# 🚀 О проекте

**Nexus Bot Platform** — это полнофункциональный сервис для развёртывания Telegram-ботов как SaaS.  
Платформа позволяет:

- создавать и запускать собственных Telegram-ботов;
- управлять конфигурациями, токенами, вебхуками;
- подключать кастомную логику;
- просматривать статистику и логи;
- использовать гибкое API интеграций;
- развернуть инфраструктуру в облаке или on-premise (Proxmox / bare metal).

Платформа построена по современным DevOps-принципам: контейнеризация, отказоустойчивость, мониторинг, логирование.

---

# 🧩 Основные компоненты

| Компонент         | Технология          | Описание |
|------------------|----------------------|----------|
| **Backend**      | FastAPI + Postgres + Redis + Celery | Бизнес-логика, управление ботами, API |
| **Frontend**     | Next.js + Tailwind   | Админ-панель, UI клиента |
| **Bot Manager**  | Python (aiogram)     | Обработчик Telegram вебхуков |
| **Proxy**        | SWAG (nginx + Lets Encrypt) | HTTPS, маршрутизация |
| **Monitoring**   | Prometheus, Grafana, Alertmanager | Метрики, алерты |
| **Logging**      | Loki + Promtail       | Централизованные логи |

---

# 🏗️ Архитектура

                ┌──────────────────────────┐
                │        Frontend          │
                │ (NextJS, Port 3000)      │
                └─────────────┬────────────┘
                              │
                      HTTPS / nginx(SWAG)
                              │
            ┌─────────────────┴───────────────────┐
            │                                     │
 ┌────────────────────┐                   ┌────────────────┐
 │      Backend       │                   │   Bot Manager  │
 │   (FastAPI:8000)   │                   │ (Webhook:8081) │
 └─────────┬──────────┘                   └────────┬───────┘
           │                                       │
 ┌─────────────────────┐                 ┌──────────────────────┐
 │    Celery Worker    │                 │     Telegram API     │
 └─────────┬───────────┘                 └──────────────────────┘
           │
   ┌──────────────────┐     ┌───────────────┐
   │     Postgres     │     │     Redis     │
   └──────────────────┘     └───────────────┘


Monitoring: Prometheus + Grafana + Alertmanager
Logs: Loki + Promtail
Reverse Proxy: SWAG (nginx + Lets Encrypt)


---

# 📦 Установка и деплой

## Требования
- Linux сервер (Ubuntu / Debian / Proxmox LXC / bare metal)
- Docker + Docker Compose
- Домен с DNS A-записью → IP сервера

## 1. Склонировать репозиторий
```bash
git clone https://github.com/ORG/REPO.git
cd REPO


## 2. Подготовить переменные окружения
Создай .env в корне:
```env
DOMAIN=example.com
POSTGRES_PASSWORD=CHANGEME
GRAFANA_ADMIN_PASSWORD=CHANGEME
TZ=Europe/Moscow
```

## 3. Запустить production-стек
```bash
./deploy_prod.sh
```

## 4. После запуска
Панель: https://example.com
Grafana: https://example.com/grafana
API: https://example.com/api

# 📚 Документация
## Backend API
Документация FastAPI автоматическая:
https://example.com/api/docs
https://example.com/api/redoc

## Основные эндпоинты:
- POST /api/bots/create — создать бота
- POST /api/bots/{id}/start — запустить
- POST /api/bots/{id}/stop — остановить
- GET /api/bots — список ботов
- GET /api/stats/{bot_id} — статистика
- POST /api/webhook/{bot_id} — вебхук

Полное описание см. docs/api.md

# 📊 Мониторинг и Observability
## Prometheus
- /metrics экспортируется backend и worker
- Alertmanager отправляет алерты в Telegram/Webhook

## Grafana включает:
- Панель производительности backend
- Панель Celery
- Панель Redis
- Панель PostgreSQL
- Логи из Loki

# 🛡️ Безопасность
Все сервисы работают в Docker bridge networks
Все внешние запросы проходят через nginx(SWAG)
HTTPS выдаётся автоматически Lets Encrypt

Жёстко рекомендуется:
сменить все пароли в .env
ограничить доступ к Grafana и Prometheus
включить Fail2Ban (опционально)

# 🧬 Структура репозитория
/
├── backend/
│   ├── app/
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   ├── public/
│   └── Dockerfile
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   ├── loki/
│   └── promtail/
├── swag/
│   └── config/
├── docker-compose.prod.yml
├── deploy_prod.sh
└── README.md

# 🤝 Контрибьютинг
PR и предложения приветствуются.
Открывайте issue, если хотите предложить улучшения.

# 📜 Лицензия
Проект распространяется под лицензией MIT.
