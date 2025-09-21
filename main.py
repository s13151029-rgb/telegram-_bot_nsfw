from fastapi import FastAPI, Request, HTTPException
import os
from redis import Redis
from rq import Queue

app = FastAPI()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required")

# koneksi Redis & queue
redis_conn = Redis.from_url(REDIS_URL)
q = Queue(connection=redis_conn)

@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != BOT_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    update = await request.json()
    # enqueue ke worker
    q.enqueue("worker.process_update", update, job_timeout=60)

    return {"ok": True}

@app.get("/")
async def index():
    return {"status": "ok"}
