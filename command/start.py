from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timezone, timedelta
from services.image_fallback import get_start_image


# ==============================
# GREETING LOGIC (VN TIME)
# ==============================

def get_greeting():
    # Giờ Việt Nam (UTC+7)
    now = datetime.now(timezone.utc) + timedelta(hours=7)
    hour = now.hour
    minute = now.minute

    # 00:00 - 10:59
    if 0 <= hour <= 10:
        return "🌅 Chào buổi sáng"

    # 11:00 - 13:00
    if hour == 11 or hour == 12 or (hour == 13 and minute == 0):
        return "🌤️ Chào buổi trưa"

    # 13:01 - 17:59
    if (hour == 13 and minute >= 1) or (14 <= hour <= 17):
        return "🌇 Chào buổi chiều"

    # 18:00 - 23:59
    return "🌙 Chào buổi tối"


# ==============================
# /START HANDLER
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    greeting = get_greeting()

    text = (
        f"{greeting}, Master 👋\n\n"
        "Em là Maidbot 🛎️\n\n"
        "Em ở đây để giúp anh thư giãn, tra cứu và khám phá những điều thú vị.\n\n"
        "📌 Gõ /help để xem các lệnh có sẵn"
    )

    image_url = get_start_image()

    # Fallback an toàn: có ảnh thì gửi ảnh, lỗi thì gửi text
    if image_url:
        try:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=image_url,
                caption=text
            )
            return
        except Exception as e:
            print("START IMAGE ERROR:", e)

    await context.bot.send_message(
        chat_id=chat_id,
        text=text
    )
