from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application
from bot import setup_handlers
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN belum diset")

WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

application = Application.builder().token(BOT_TOKEN).build()
setup_handlers(application)

@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.start()

@app.on_event("shutdown")
async def on_shutdown():
    await application.stop()
    await application.shutdown()

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return {"ok": True}
    except Exception as e:
        print("❌ Webhook processing error:", e)
        return {"ok": False, "error": str(e)}
