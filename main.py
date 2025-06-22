from fastapi import FastAPI, Request
import telegram
from bot import application
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

@app.post(WEBHOOK_PATH)
async def process_update(request: Request):
    data = await request.json()
    update = telegram.Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"ok": True}