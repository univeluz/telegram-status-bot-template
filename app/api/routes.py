import logging

from fastapi import APIRouter, Header, HTTPException, Request, status

from app.config.settings import Settings
from app.services.health_service import build_health_response
from app.services.update_service import TelegramUpdateError, process_webhook_update

logger = logging.getLogger(__name__)

router = APIRouter()


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


@router.get("/")
async def root(request: Request) -> dict[str, object]:
    settings = get_settings(request)
    return build_health_response(settings)


@router.get("/health")
async def health(request: Request) -> dict[str, object]:
    settings = get_settings(request)
    return build_health_response(settings)


@router.post("/webhook")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict[str, bool]:
    settings = get_settings(request)
    if x_telegram_bot_api_secret_token != settings.webhook_secret_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Telegram webhook secret token.",
        )

    try:
        payload = await request.json()
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Webhook body must be valid JSON.",
        ) from exc

    if not isinstance(payload, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Webhook payload must be a JSON object.",
        )

    try:
        await process_webhook_update(request.app.state.bot, payload)
    except TelegramUpdateError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Webhook payload is not a valid Telegram update.",
        ) from None
    except Exception:
        logger.exception("Unhandled error while processing Telegram webhook update")

    return {"ok": True}
