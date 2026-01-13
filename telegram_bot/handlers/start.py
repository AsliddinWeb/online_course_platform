from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from services.api import backend_api


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start command handler.
    Deep link bilan kelsa - OTP yuboradi.
    Oddiy /start bo'lsa - salomlashadi.
    """
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Deep link tokenni olish
    args = context.args

    if args and len(args) > 0:
        # Deep link bilan kelgan
        token = args[0]
        await handle_deep_link(update, context, token, chat_id)
    else:
        # Oddiy /start
        await send_welcome_message(update, context)


async def handle_deep_link(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        token: str,
        chat_id: int
) -> None:
    """Deep link orqali kelgan foydalanuvchini tekshirish va OTP yuborish"""

    # Loading message
    loading_msg = await update.message.reply_text(
        "⏳ Tekshirilmoqda..."
    )

    # Backend ga so'rov
    result = await backend_api.verify_deep_link(token, chat_id)

    # Loading message ni o'chirish
    await loading_msg.delete()

    if result and result.get('success'):
        otp_code = result.get('otp_code')
        full_name = result.get('full_name', 'Foydalanuvchi')

        # OTP ni yuborish
        message = (
            f"👋 Salom, <b>{full_name}</b>!\n\n"
            f"🔐 Sizning tasdiqlash kodingiz:\n\n"
            f"<code>{otp_code}</code>\n\n"
            f"⏱ Kod 2 daqiqa ichida amal qiladi.\n\n"
            f"☝️ Kodni saytdagi maydonchaga kiriting."
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Qayta yuborish", callback_data="resend_otp")]
        ])

        await update.message.reply_text(
            message,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    else:
        # Xatolik
        await update.message.reply_text(
            "❌ Xatolik yuz berdi.\n\n"
            "Iltimos, saytdan qaytadan urinib ko'ring yoki admin bilan bog'laning.",
            parse_mode='HTML'
        )


async def send_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Oddiy salomlashuv xabari"""
    user = update.effective_user

    message = (
        f"👋 Salom, <b>{user.first_name}</b>!\n\n"
        f"Bu <b>EduPlatform</b> rasmiy boti.\n\n"
        f"📚 Platforma orqali:\n"
        f"• Video darslarni ko'ring\n"
        f"• O'z progressingizni kuzating\n"
        f"• Bilimlaringizni oshiring\n\n"
        f"🔐 Tizimga kirish uchun saytga boring va telefon raqamingizni kiriting."
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Saytga o'tish", url="https://eduplatform.uz")]
    ])

    await update.message.reply_text(
        message,
        parse_mode='HTML',
        reply_markup=keyboard
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/help command handler"""

    message = (
        "ℹ️ <b>Yordam</b>\n\n"
        "Bu bot <b>EduPlatform</b> tizimiga kirish uchun tasdiqlash kodlarini yuboradi.\n\n"
        "<b>Qanday foydalanish:</b>\n"
        "1. Saytga boring\n"
        "2. Telefon raqamingizni kiriting\n"
        "3. Telegram havolasini bosing\n"
        "4. Botdan kelgan kodni saytga kiriting\n\n"
        "<b>Buyruqlar:</b>\n"
        "/start - Botni ishga tushirish\n"
        "/help - Yordam\n\n"
        "Savollar bo'lsa: @admin_username"
    )

    await update.message.reply_text(message, parse_mode='HTML')