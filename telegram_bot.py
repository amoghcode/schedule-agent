from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
import os

load_dotenv()
bot_token = os.getenv("TELGRAM_BOT_TOKEN")

app = ApplicationBuilder().token(bot_token).build()

async def handle_message(update, context):
    text = update.message.text
    response = text
    await update.message.reply_text(response)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

app.run_polling()


