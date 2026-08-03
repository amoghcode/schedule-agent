import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import telegram_bot


class TelegramMessageHandlerTests(unittest.IsolatedAsyncioTestCase):
    def make_update(
        self,
        text="Show my calendar",
        user_id=123,
        chat_id=456,
    ):
        message = SimpleNamespace(
            text=text,
            reply_text=AsyncMock(),
        )

        update = SimpleNamespace(
            effective_message=message,
            effective_user=SimpleNamespace(id=user_id),
            effective_chat=SimpleNamespace(id=chat_id),
        )

        return update, message

    @staticmethod
    def make_context(allowed_user_id=None):
        return SimpleNamespace(
            application=SimpleNamespace(
                bot_data={"allowed_user_id": allowed_user_id}
            )
        )

    async def test_authorized_message_is_forwarded(self):
        update, message = self.make_update()
        context = self.make_context(allowed_user_id=123)

        with patch(
            "telegram_bot.ask_scheduler",
            new=AsyncMock(return_value="You have no events."),
        ) as ask_scheduler:
            await telegram_bot.handle_message(update, context)

        ask_scheduler.assert_awaited_once_with(
            "Show my calendar",
            user_id="123",
            session_id="456",
        )

        message.reply_text.assert_awaited_once_with(
            "You have no events."
        )

    async def test_unauthorized_user_is_rejected(self):
        update, message = self.make_update(user_id=999)
        context = self.make_context(allowed_user_id=123)

        with patch(
            "telegram_bot.ask_scheduler",
            new=AsyncMock(),
        ) as ask_scheduler:
            await telegram_bot.handle_message(update, context)

        ask_scheduler.assert_not_awaited()
        message.reply_text.assert_awaited_once_with(
            "Sorry, this bot is private."
        )

    async def test_access_is_open_without_allowlist(self):
        update, message = self.make_update(user_id=999)
        context = self.make_context()

        with patch(
            "telegram_bot.ask_scheduler",
            new=AsyncMock(return_value="Hello"),
        ) as ask_scheduler:
            await telegram_bot.handle_message(update, context)

        ask_scheduler.assert_awaited_once()
        message.reply_text.assert_awaited_once_with("Hello")

    async def test_blank_message_is_rejected(self):
        update, message = self.make_update(text="   ")
        context = self.make_context()

        with patch(
            "telegram_bot.ask_scheduler",
            new=AsyncMock(),
        ) as ask_scheduler:
            await telegram_bot.handle_message(update, context)

        ask_scheduler.assert_not_awaited()
        message.reply_text.assert_awaited_once_with(
            "Please send a non-empty text message."
        )

    async def test_agent_error_returns_safe_message(self):
        update, message = self.make_update()
        context = self.make_context()

        with patch(
            "telegram_bot.ask_scheduler",
            new=AsyncMock(
                side_effect=RuntimeError("agent unavailable")
            ),
        ):
            await telegram_bot.handle_message(update, context)

        message.reply_text.assert_awaited_once_with(
            "Sorry, the scheduling agent could not process that message. "
            "Please try again."
        )


class SettingsTests(unittest.TestCase):
    @patch.dict(
        "os.environ",
        {
            "TELEGRAM_BOT_TOKEN": "telegram-token",
            "GOOGLE_API_KEY": "google-key",
            "ALLOWED_TELEGRAM_USER_ID": "123",
        },
        clear=True,
    )
    def test_load_settings_parses_allowed_user(self):
        settings = telegram_bot.load_settings()

        self.assertEqual(
            settings.telegram_bot_token,
            "telegram-token",
        )
        self.assertEqual(
            settings.allowed_telegram_user_id,
            123,
        )

    @patch.dict(
        "os.environ",
        {"GOOGLE_API_KEY": "google-key"},
        clear=True,
    )
    def test_missing_telegram_token_is_rejected(self):
        with patch("telegram_bot.load_dotenv"):
            with self.assertRaisesRegex(
                RuntimeError,
                "TELEGRAM_BOT_TOKEN",
        ):
                telegram_bot.load_settings()

    @patch.dict(
        "os.environ",
        {"TELEGRAM_BOT_TOKEN": "telegram-token"},
        clear=True,
    )
    def test_missing_google_api_key_is_rejected(self):
        with patch("telegram_bot.load_dotenv"):
            with self.assertRaisesRegex(
                RuntimeError,
                "GOOGLE_API_KEY",
        ):
                telegram_bot.load_settings()

    @patch.dict(
        "os.environ",
        {
            "TELEGRAM_BOT_TOKEN": "telegram-token",
            "GOOGLE_API_KEY": "google-key",
            "ALLOWED_TELEGRAM_USER_ID": "not-a-number",
        },
        clear=True,
    )
    def test_invalid_allowed_user_is_rejected(self):
        with self.assertRaisesRegex(
            RuntimeError,
            "ALLOWED_TELEGRAM_USER_ID",
        ):
            telegram_bot.load_settings()


if __name__ == "__main__":
    unittest.main()