import os
import time
import openai
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

COOLDOWN = 3
last_reply = 0

def handle_message(update, context):
    global last_reply

    if not update.message or not update.message.text:
        return

    now = time.time()
    if now - last_reply < COOLDOWN:
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Reply like a normal human. Short."},
                {"role": "user", "content": update.message.text}
            ],
            max_tokens=80
        )

        update.message.reply_text(
            response.choices[0].message.content.strip()
        )

        last_reply = now

    except Exception as e:
        print("OpenAI error:", e)


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
