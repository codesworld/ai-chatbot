import os
from openai import OpenAI
from dotenv import load_dotenv
from app.database import get_history, save_message

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. "
    "You can communicate in English. "
    "Give short, clear, and helpful answers."
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")


def get_response(message: str, session_id: str) -> str:
    save_message(session_id, "user", message)

    history = get_history(session_id)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
    )

    assistant_message = completion.choices[0].message.content
    save_message(session_id, "assistant", assistant_message)
    return assistant_message
