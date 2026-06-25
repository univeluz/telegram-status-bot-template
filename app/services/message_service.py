from app.config.settings import get_settings


def get_start_message() -> str:
    return get_settings().start_message
