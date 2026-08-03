import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

from scheduler.agent import ask_scheduler


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    allowed_telegram_user_id: int | None


def load_settings() -> Settings:
    """Load and validate settings needed to start the Telegram bot."""
    load_dotenv()

    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing or empty.")

    google_api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is missing or empty.")

    allowed_user_id_value = os.getenv(
        "ALLOWED_TELEGRAM_USER_ID",
        "",
    ).strip()

    if allowed_user_id_value:
        try:
            allowed_user_id = int(allowed_user_id_value)
        except ValueError as error:
            raise RuntimeError(
                "ALLOWED_TELEGRAM_USER_ID must be a numeric Telegram user ID."
            ) from error
    else:
        allowed_user_id = None

    return Settings(
        telegram_bot_token=telegram_bot_token,
        allowed_telegram_user_id=allowed_user_id,
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Authorize and forward a Telegram text message to the scheduler."""
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    if message is None or user is None or chat is None:
        LOGGER.warning(
            "Ignoring Telegram update without message, user, or chat."
        )
        return

    allowed_user_id = context.application.bot_data.get("allowed_user_id")

    if allowed_user_id is not None and user.id != allowed_user_id:
        await reply_safely(message, "Sorry, this bot is private.")
        return

    text = (message.text or "").strip()

    if not text:
        await reply_safely(
            message,
            "Please send a non-empty text message.",
        )
        return

    try:
        response = await ask_scheduler(
            text,
            user_id=str(user.id),
            session_id=str(chat.id),
        )
    except Exception:
        LOGGER.exception(
            "Scheduler failed while handling a Telegram message."
        )
        await reply_safely(
            message,
            "Sorry, the scheduling agent could not process that message. "
            "Please try again.",
        )
        return

    await reply_safely(message, response)


async def reply_safely(message, text: str) -> None:
    """Send a Telegram response while handling Telegram API failures."""
    try:
        await message.reply_text(text)
    except TelegramError:
        LOGGER.exception("Telegram failed to send a bot response.")


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Log errors not handled by an update handler."""
    LOGGER.error(
        "Unhandled Telegram update error.",
        exc_info=(
            type(context.error),
            context.error,
            context.error.__traceback__,
        )
        if context.error
        else None,
    )


def build_application(settings: Settings) -> Application:
    """Build the Telegram application without starting polling."""
    application = (
        ApplicationBuilder()
        .token(settings.telegram_bot_token)
        .build()
    )

    application.bot_data["allowed_user_id"] = (
        settings.allowed_telegram_user_id
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )
    application.add_error_handler(error_handler)

    return application


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=logging.INFO,
    )

    try:
        settings = load_settings()
        application = build_application(settings)
    except RuntimeError as error:
        raise SystemExit(f"Configuration error: {error}") from error

    LOGGER.info("Starting Telegram bot polling.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()