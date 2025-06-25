from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application
from bot import setup_handlers
import os

# Inisialisasi FastAPI
app = FastAPI()

# Load BOT_TOKEN dari environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN belum diset")

# Build Application (bot)
application = Application.builder().token(BOT_TOKEN).build()

# Daftarkan semua handler (dari bot.py)
setup_handlers(application)

# Webhook path spesifik (untuk keamanan)
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

# Event: Saat Vercel/instance dijalankan
@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.start()

# Event: Saat shutdown
@app.on_event("shutdown")
async def on_shutdown():
    await application.stop()
    await application.shutdown()

# Endpoint utama untuk menerima update dari Telegram
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}
