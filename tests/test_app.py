from collections.abc import AsyncIterator

import pytest
from aiogram import Bot
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with app.router.lifespan_context(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as value:
            yield value


async def test_health_endpoint(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "telegram-status-bot"
    assert body["runtime"]["environment"] == "production"


async def test_webhook_rejects_invalid_secret(client: AsyncClient) -> None:
    response = await client.post(
        "/webhook",
        headers={"X-Telegram-Bot-Api-Secret-Token": "wrong-secret"},
        json={"update_id": 1},
    )

    assert response.status_code == 403


async def test_webhook_rejects_invalid_payload(client: AsyncClient) -> None:
    response = await client.post(
        "/webhook",
        headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret-token"},
        json=["not", "an", "object"],
    )

    assert response.status_code == 400


async def test_webhook_accepts_valid_update(
    client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    processed_updates: list[int] = []

    async def fake_process_webhook_update(
        bot: Bot,
        payload: dict[str, object],
    ) -> None:
        assert bot is app.state.bot
        processed_updates.append(int(payload["update_id"]))

    monkeypatch.setattr(
        "app.api.routes.process_webhook_update",
        fake_process_webhook_update,
    )

    response = await client.post(
        "/webhook",
        headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret-token"},
        json={"update_id": 42},
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert processed_updates == [42]


def test_bot_initialized_in_lifespan() -> None:
    assert app.router.lifespan_context is not None
