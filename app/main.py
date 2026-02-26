from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.models import ChatRequest, ChatResponse
from app.chat import get_response
from app.database import init_db, clear_history

app = FastAPI(title="AI Chatbot")


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/")
async def root():
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = get_response(request.message, request.session_id)
    return ChatResponse(response=response, session_id=request.session_id)


@app.delete("/chat/{session_id}")
async def clear_chat(session_id: str):
    clear_history(session_id)
    return {"message": "History cleared", "session_id": session_id}
