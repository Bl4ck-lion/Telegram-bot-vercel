import os
import requests
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === Konfigurasi Token ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    print("✅ /start diterima")
    try:
        res = requests.get("https://api.waifu.pics/sfw/waifu").json()
        waifu_image_url = res["url"]
    except Exception:
        waifu_image_url = None

    keyboard = [[InlineKeyboardButton("Menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if waifu_image_url:
        await update.message.reply_photo(
            photo=waifu_image_url,
            caption="🎉 Halo! Saya siap membantu Anda.\nGunakan tombol atau ketik command.",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "🎉 Halo! Saya siap membantu Anda.\n(Gagal memuat gambar waifu 🥲)",
            reply_markup=reply_markup
        )


# === /waifu ===
async def waifu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    print("✅ /waifu diterima")
    try:
        res = requests.get("https://api.waifu.pics/sfw/waifu").json()
        await update.message.reply_photo(photo=res["url"], caption="Here's your waifu 💖")
    except:
        await update.message.reply_text("Gagal mengambil waifu 😿")


# === /meme ===
async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    print("✅ /meme diterima")
    try:
        res = requests.get("https://meme-api.com/gimme").json()
        title = res.get("title")
        post_link = res.get("postLink")
        meme_url = res.get("url")
        caption = f"{title}\n{post_link}"
        await update.message.reply_photo(photo=meme_url, caption=caption)
    except:
        await update.message.reply_text("Gagal mengambil meme 😅")


# === /translate <teks> ===
async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    print("✅ /translate diterima")
    if not context.args:
        await update.message.reply_text("Gunakan format: /translate <teks>")
        return

    text = ' '.join(context.args)
    try:
        res = requests.post("https://de.libretranslate.com/translate", data={
            "q": text,
            "source": "auto",
            "target": "de",
            "format": "text"
        }).json()
        await update.message.reply_text(f"🇩🇪 {res['translatedText']}")
    except:
        await update.message.reply_text("Terjadi kesalahan saat menerjemahkan.")


# === AI reply (tanpa command) ===
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    print("💬 Pesan masuk untuk GPT:", update.message.text)
    if not OPENAI_API_KEY:
        await update.message.reply_text("AI tidak aktif karena OPENAI_API_KEY belum diset.")
        return

    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kamu adalah asisten Telegram yang ramah."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )
        reply_text = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply_text.strip())
    except Exception as e:
        await update.message.reply_text("❌ Gagal mendapatkan respons dari GPT.")
        print("❌ GPT Error:", e)


# === Fungsi untuk mendaftarkan semua handler ===
def setup_handlers(app: Application):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("waifu", waifu))
    app.add_handler(CommandHandler("meme", meme))
    app.add_handler(CommandHandler("translate", translate))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
