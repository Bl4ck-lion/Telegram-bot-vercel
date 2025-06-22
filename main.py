from fastapi import FastAPI, Request
from bot import application
import telegram
import os

from telegram import Update

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

# Jalankan bot saat Vercel instance start
@app.on_event("startup")
async def startup():
    await application.initialize()
    await application.start()

# Hentikan bot dengan aman saat shutdown
@app.on_event("shutdown")
async def shutdown():
    await application.stop()
    await application.shutdown()

# Endpoint untuk menerima update dari Telegram
@app.post(WEBHOOK_PATH)
async def process_update(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}
