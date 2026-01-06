from telegram import Update
from telegram.ext import ContextTypes
from services.image_fallback import get_start_image


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    text = (
        "🛎️ Chào mừng anh đã gọi Maidbot\n\n"
        "Em ở đây để giúp anh thư giãn, tra cứu và khám phá những điều thú vị.\n"
        "Gõ /help để xem các lệnh có sẵn."
    )

    image_url = get_start_image()

    if image_url:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_url,
            caption=text
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text
        )

