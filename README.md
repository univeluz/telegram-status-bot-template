# Telegram Status Bot Template

Production-ready FastAPI and Aiogram template for webhook-only Telegram bots. The project is intentionally small, explicit, and deployment-focused: no polling, no hidden configuration, no hardcoded secrets, and no unnecessary runtime dependencies.

## Architecture

The application is split into three layers:

- `app/api/`: FastAPI routes for `/`, `/health`, and `/webhook`.
- `app/bot/`: Aiogram dispatcher and handlers.
- `app/services/`: webhook synchronization, update processing, health payloads, and response message access.
- `app/config/`: environment-driven settings and logging setup.
- `app/main.py`: FastAPI application entrypoint with lifespan startup and shutdown.

Routes stay HTTP-focused, handlers stay Telegram-focused, and shared behavior flows through the service layer.

## Requirements

- Python 3.13
- uv
- A Telegram bot token from BotFather
- A public HTTPS application URL for Telegram webhooks

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `BOT_TOKEN` | Yes | Telegram bot token. |
| `APP_URL` | Yes | Public HTTPS base URL, for example `https://bot.example.com`. |
| `WEBHOOK_SECRET_TOKEN` | Yes | Strong random token validated against Telegram's `X-Telegram-Bot-Api-Secret-Token` header. |
| `START_MESSAGE` | Yes | Message sent when a user runs `/start`. |
| `WEBHOOK_PATH` | No | Webhook route. Must remain `/webhook`. |
| `DROP_PENDING_UPDATES_ON_STARTUP` | No | Drop pending Telegram updates during webhook synchronization. Defaults to `false`. |
| `DELETE_WEBHOOK_BEFORE_SET` | No | Delete any existing webhook before setting the current one. Defaults to `true`. |
| `DELETE_WEBHOOK_ON_SHUTDOWN` | No | Delete webhook during application shutdown. Defaults to `false`. |
| `SYNC_WEBHOOK_ON_STARTUP` | No | Synchronize Telegram webhook on application startup. Defaults to `true`. |
| `LOG_LEVEL` | No | Python logging level. Defaults to `INFO`. |
| `SERVICE_NAME` | No | Name returned by health endpoints. Defaults to `telegram-status-bot`. |
| `ENVIRONMENT` | No | Runtime environment label. Defaults to `production`. |

## Local Setup

Create a `.env` file from `.env.example`, then install dependencies:

```bash
uv sync
```

Run the app:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For local development without a public HTTPS URL, keep `SYNC_WEBHOOK_ON_STARTUP=false` until you expose the app with a trusted tunnel or deploy it.

## Webhook Flow

On startup, the lifespan manager creates one Aiogram bot instance and synchronizes Telegram's webhook to:

```text
APP_URL + WEBHOOK_PATH
```

Telegram sends updates to `POST /webhook` with `X-Telegram-Bot-Api-Secret-Token`. Invalid or missing tokens receive `403`. Malformed payloads receive `400`. Valid webhook requests always receive `200`, even if update handling logs an internal exception.

The template never starts polling.

## Docker

Build and run:

```bash
docker build -t telegram-status-bot-template .
docker run --env-file .env -p 8000:8000 telegram-status-bot-template
```

Local compose:

```bash
docker compose up --build
```

The production image uses `python:3.13-slim`, installs runtime dependencies with uv, and exposes port `8000`.

## Railway

Railway can deploy directly from GitHub. Configure the environment variables in Railway, including `PORT` if Railway does not inject it automatically.

Use this start command:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set `APP_URL` to the Railway public HTTPS domain.

## VPS

Install uv using the official installer, sync dependencies, and run Uvicorn:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --frozen --no-dev
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For systemd, run the same Uvicorn command from the repository directory and provide environment variables through an environment file owned by the deployment user.

## Vercel

Vercel compatibility is provided through `requirements.txt` and `vercel.json`. The FastAPI ASGI app is exposed as `app` in `app/main.py`, and Vercel installs dependencies from `requirements.txt` without relying on uv at runtime.

Set all required environment variables in the Vercel project dashboard. `APP_URL` must be the public Vercel HTTPS URL.

## Quality Checks

Run:

```bash
uv run ruff check .
uv run pytest
uv run python -m compileall app tests
```

The GitHub Actions workflow installs Python 3.13, installs uv, syncs dependencies with `uv sync --frozen`, runs Ruff, and verifies import safety.

## Security Notes

- Keep `BOT_TOKEN` and `WEBHOOK_SECRET_TOKEN` out of source control.
- Use a long random `WEBHOOK_SECRET_TOKEN`.
- Only `/`, `/health`, and `/webhook` are exposed.
- The webhook endpoint validates Telegram's secret token header before parsing updates.
- Configuration fails fast when required environment variables are missing.
