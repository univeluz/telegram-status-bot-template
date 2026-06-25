from datetime import UTC, datetime

from app.config.settings import Settings


def build_health_response(settings: Settings) -> dict[str, object]:
    return {
        "status": "ok",
        "service": settings.service_name,
        "runtime": {
            "environment": settings.environment,
            "timestamp": datetime.now(UTC).isoformat(),
        },
    }
