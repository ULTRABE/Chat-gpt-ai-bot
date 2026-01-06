import os
import time
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

LAST_REPLY = 0
COOLDOWN = 3  # seconds

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global LAST_REPLY
    now = time.time()

    if now - LAST_REPLY < COOLDOWN:
        return

    if update.message is None:
        return

    text = update.message.text
    if not text:
        return

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Reply like a normal human, short and casual."},
            {"role": "user", "content": text}
        ]
    )

    await update.message.reply_text(
        response.choices[0].message.content.strip()
    )

    LAST_REPLY = now

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
