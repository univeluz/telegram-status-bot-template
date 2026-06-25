# Telegram Status Bot Template — Agent Instructions

## 1. Project Mission

This repository is a production-grade, webhook-only Telegram bot template built with:

- Python 3.13
- FastAPI
- Aiogram 3.x
- uv dependency manager

The goal is to provide a clean, scalable, deployment-ready foundation for real-world Telegram bots running in production environments (Railway, Docker, VPS, Vercel).

The system must always prioritize:

- reliability over complexity
- explicit behavior over magic
- minimal dependencies
- production safety
- predictable architecture

---

## 2. Core Principles

Every implementation in this repository MUST follow these principles:

### 2.1 No Polling Policy
The bot MUST NEVER use polling mode under any circumstance.
Only webhook-based architecture is allowed.

### 2.2 Explicit Configuration
All runtime configuration MUST be loaded from environment variables.
No hardcoded secrets, tokens, URLs, or messages.

### 2.3 Minimal Dependencies
Only include dependencies that are strictly required for runtime.
Avoid bloated libraries or redundant abstractions.

### 2.4 Production First
All code must assume production deployment:
- concurrency-safe
- stateless where possible
- fast startup time
- proper shutdown handling

---

## 3. Architecture Overview

The system is split into three main layers:

### 3.1 API Layer (FastAPI)
Responsible for:
- HTTP server
- webhook endpoint
- health checks
- Telegram update ingestion

### 3.2 Bot Layer (Aiogram)
Responsible for:
- message handling
- command routing
- Telegram interaction logic

### 3.3 Service Layer
Responsible for:
- webhook synchronization
- Telegram API integration
- external communication logic

---

## 4. Folder Structure Rules

The repository MUST follow this structure:

app/
  api/         → FastAPI routes only
  bot/         → Aiogram logic only
  config/      → Settings and environment parsing
  services/    → External integrations
  main.py      → Application entrypoint

Rules:
- No cross-layer imports except via services
- No business logic inside routes
- No Telegram logic inside API layer
# Telegram Status Bot Template — Agent Instructions

## 5. Coding Standards

All code in this repository MUST follow strict Python engineering standards.

### 5.1 Python Version
- Python 3.13 only
- No compatibility hacks for older versions

### 5.2 Type Hints
- All functions MUST use type hints
- No untyped public functions
- Prefer built-in generics (list, dict) over typing.List

### 5.3 Code Style
- Follow PEP 8 strictly
- Use Ruff as the primary linter
- No unused imports
- No dead code
- No commented-out blocks in final code

### 5.4 Naming Conventions
- snake_case for functions and variables
- PascalCase for classes
- UPPER_CASE for constants
- No abbreviations unless widely accepted (e.g., HTTP, API)

---

## 6. FastAPI Rules

### 6.1 Lifespan Management
- MUST use FastAPI lifespan context manager
- No deprecated startup/shutdown events

### 6.2 Routes
Allowed routes only:

- GET /
- GET /health
- POST /webhook

No additional routes unless explicitly required.

### 6.3 Webhook Endpoint
- Must validate Telegram secret token header
- Must reject invalid requests with 403
- Must parse updates safely
- Must not block event loop

### 6.4 Health Endpoint
Must return structured JSON:
- status
- service name
- runtime info

---

## 7. Aiogram Rules

### 7.1 Dispatcher
- Single global Dispatcher instance only
- No multiple bot instances

### 7.2 Handlers
- All handlers MUST be isolated in bot/handlers.py
- No business logic inside handlers
- Handlers must call service layer only

### 7.3 Commands
- /start is required
- /start message must come from environment variable START_MESSAGE

---

## 8. Webhook Synchronization Rules

On application startup:

1. Remove existing webhook (optional based on config)
2. Set new webhook using APP_URL + WEBHOOK_PATH
3. Attach SECRET TOKEN header validation
4. Log success or failure

On shutdown:
- Optionally delete webhook if DELETE_WEBHOOK_ON_SHUTDOWN=true

---

## 9. Security Rules

### 9.1 Telegram Secret Token
- Must validate X-Telegram-Bot-Api-Secret-Token header
- Must reject all requests without valid token

### 9.2 Environment Variables
- No secrets in code
- No fallback production secrets
- Fail fast if required env vars are missing

### 9.3 Input Validation
- Never trust incoming Telegram payload
- Validate structure before processing

---

## 10. Error Handling

- No silent failures
- All exceptions must be logged
- Webhook must always return HTTP 200 if request is valid (even if handler fails)
- Invalid requests return HTTP 400 or 403
# Telegram Status Bot Template — Agent Instructions

## 11. Deployment Rules

### 11.1 Docker

The project MUST include:
- Dockerfile (production optimized)
- docker-compose.yml (local development)

Rules:
- No dev dependencies in production image
- Use slim Python base image
- Use uv for dependency installation
- Expose only required port (default: 8000)

---

### 11.2 Railway Deployment

Requirements:
- Must support automatic deployment from GitHub
- Must use PORT environment variable
- Must run via uvicorn with host 0.0.0.0

Startup command:
uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT

---

### 11.3 VPS Deployment

Rules:
- Must support systemd or manual uvicorn run
- Must not require Docker (optional only)
- Must support uv installation via official script

---

### 11.4 Vercel Deployment

Constraints:
- Must use requirements.txt for compatibility
- Must NOT rely on uv in Vercel runtime
- Must expose FastAPI app as ASGI handler

---

## 12. CI/CD Rules

A GitHub Actions workflow MUST exist.

Pipeline steps:
1. Setup Python 3.13
2. Install uv
3. Sync dependencies (uv sync --frozen)
4. Run linting (ruff)
5. Ensure import safety

Pipeline MUST fail on:
- lint errors
- missing imports
- syntax errors

---

## 13. Dependency Management

### Source of truth:
- pyproject.toml

### Lock file:
- uv.lock (must always be committed)

### Vercel fallback:
- requirements.txt (auto-maintained or manually synced)

No other dependency sources allowed.

---

## 14. Logging Rules

- Structured logging preferred
- No print() in production code
- Logs must include:
  - timestamp
  - log level
  - module name

Log levels:
- INFO for normal lifecycle
- WARNING for recoverable issues
- ERROR for failures

---

## 15. Testing Rules (Optional but recommended)

If tests exist:
- Must use pytest
- Must be async-aware (pytest-asyncio)
- Must not require external services

Tests should cover:
- webhook endpoint
- health endpoint
- basic bot initialization

---

## 16. Git Conventions

Commit messages MUST follow:

- feat: new feature
- fix: bug fix
- refactor: code restructuring
- chore: maintenance
- docs: documentation changes

No vague messages like "update" or "fix stuff".

---

## 17. README Requirements

README.md MUST include:

- Project overview
- Architecture explanation
- Setup instructions (uv-based)
- Docker instructions
- Railway deployment guide
- VPS deployment guide
- Vercel deployment guide
- Environment variables table
- Webhook explanation
- Security notes

README must be production-grade, not minimal.

---

## 18. Final Rule (Most Important)

If any instruction conflicts with convenience, readability, or shortcuts:

👉 ALWAYS prioritize production safety, clarity, and correctness.
