import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

from config import BOT_TOKEN
from handlers import start_handler, help_handler
from handlers.otp import resend_otp_handler

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Bot ni ishga tushirish"""

    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))

    # Callback query handlers
    application.add_handler(CallbackQueryHandler(resend_otp_handler, pattern="^resend_otp$"))

    # Bot ni ishga tushirish
    logger.info("Bot ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()