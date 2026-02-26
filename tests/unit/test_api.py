import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_chat_endpoint():
    with patch("app.main.get_response", return_value="Hello! How can I help you?"):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/chat",
                json={"message": "Hello", "session_id": "test_session"},
            )
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Hello! How can I help you?"
    assert data["session_id"] == "test_session"


@pytest.mark.asyncio
async def test_chat_default_session():
    with patch("app.main.get_response", return_value="Answer"):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/chat",
                json={"message": "Test"},
            )
    assert response.status_code == 200
    assert response.json()["session_id"] == "default"


@pytest.mark.asyncio
async def test_clear_chat():
    with patch("app.main.clear_history") as mock_clear:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.delete("/chat/test_session")
        mock_clear.assert_called_once_with("test_session")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test_session"


@pytest.mark.asyncio
async def test_chat_missing_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/chat", json={})
    assert response.status_code == 422
