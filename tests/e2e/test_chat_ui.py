import pytest
from playwright.sync_api import Page, expect


# The application must be running before executing e2e tests:
# uvicorn app.main:app --reload --port 8000


BASE_URL = "http://localhost:8000"


def test_page_loads(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title("AI Chatbot")


def test_input_and_send_button_visible(page: Page):
    page.goto(BASE_URL)
    expect(page.locator("#message-input")).to_be_visible()
    expect(page.locator("#send-button")).to_be_visible()


def test_send_message_appears_in_chat(page: Page):
    page.goto(BASE_URL)
    page.fill("#message-input", "Hello")
    page.click("#send-button")
    expect(page.locator(".message.user").first).to_contain_text("Hello")


def test_clear_chat_button(page: Page):
    page.goto(BASE_URL)
    page.fill("#message-input", "Test message")
    page.click("#send-button")
    # Click the clear button
    page.click(".clear-btn")
    # Verify messages are cleared
    expect(page.locator(".message")).to_have_count(0)
