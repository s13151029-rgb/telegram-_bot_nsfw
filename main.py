from fastapi import FastAPI, Request, HTTPException
import os
import json
import requests

app = FastAPI()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required")

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    url = f"{API_BASE}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()

def extract_chat_id_from_update(update: dict):
    if "message" in update:
        chat = update["message"].get("chat", {})
        return chat.get("id"), chat.get("type")
    if "channel_post" in update:
        chat = update["channel_post"].get("chat", {})
        return chat.get("id"), chat.get("type")
    return None, None

def process_update(update: dict):
    print("Processing:", json.dumps(update))
    chat_id, chat_type = extract_chat_id_from_update(update)
    if chat_id:
        text = f"Chat type: {chat_type}\nID: {chat_id}"
        send_message(chat_id, text)

@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != BOT_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    update = await request.json()
    process_update(update)
    return {"ok": True}

@app.get("/")
async def index():
    return {"status": "ok"}
