# Telegram Bot on Vercel (Python + FastAPI)

Deploy your Telegram bot using Python, FastAPI, and Vercel!

## 🧪 Features
- ✅ Python 3
- ✅ FastAPI
- ✅ Webhook-based
- ✅ Hosted on Vercel

## 🚀 Deploy

1. Clone this repo
2. Create `.env` file locally (optional, for local testing)
3. Set `BOT_TOKEN` environment variable on Vercel Dashboard
4. Deploy with:

```bash
vercel deploy --prod
```

5. Set the webhook:

```bash
curl "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://your-vercel-url.vercel.app/webhook/<YOUR_TOKEN>"
```

## 🛠 File Structure

- `bot.py`: Telegram logic
- `main.py`: FastAPI server
- `requirements.txt`: Python dependencies
- `vercel.json`: Vercel config

## 💬 Example

Try sending `/start` to your bot!