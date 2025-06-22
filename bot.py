from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

application = Application.builder().token(BOT_TOKEN).build()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Bot ini berhasil jalan di Vercel 🚀")

# Tambahkan handler ke bot
application.add_handler(CommandHandler("start", start))