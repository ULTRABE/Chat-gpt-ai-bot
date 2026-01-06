import os
import time
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

# Load env locally (Railway ignores .env and uses Variables)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

COOLDOWN = 3
last_reply_time = 0

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_reply_time

    if not update.message or not update.message.text:
        return

    now = time.time()
    if now - last_reply_time < COOLDOWN:
        return

    user_text = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Reply like a real human. Short and casual."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=80
        )

        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)

        last_reply_time = now

    except Exception as e:
        print("OpenAI error:", e)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()
