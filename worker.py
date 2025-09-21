import os
import json
import requests
from redis import Redis
from rq import Worker, Queue, Connection

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required")

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    url = f"{API_BASE}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_notification": True,
    }
    r = requests.post(url, json=payload, timeout=10)
    try:
        r.raise_for_status()
    except Exception as e:
        print("Failed to send message", r.status_code, r.text)
        raise
    return r.json()

def extract_chat_id_from_update(update: dict):
    if "message" in update:
        chat = update["message"].get("chat", {})
        return chat.get("id"), chat.get("type")
    if "channel_post" in update:
        chat = update["channel_post"].get("chat", {})
        return chat.get("id"), chat.get("type")
    if "edited_message" in update:
        chat = update["edited_message"].get("chat", {})
        return chat.get("id"), chat.get("type")
    return None, None

def process_update(update: dict):
    print("Processing update:", json.dumps(update))
    chat_id, chat_type = extract_chat_id_from_update(update)
    if chat_id is None:
        return {"error": "no_chat"}

    text = f"Chat type: {chat_type}\nID: {chat_id}"
    try:
        resp = send_message(chat_id, text)
        print("Sent message response:", resp)
        return resp
    except Exception as e:
        print("Error sending message:", e)
        return {"error": str(e)}

# kalau dijalankan langsung -> start worker
if __name__ == "__main__":
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    conn = Redis.from_url(redis_url)
    with Connection(conn):
        q = Queue()
        worker = Worker(q)
        worker.work()
