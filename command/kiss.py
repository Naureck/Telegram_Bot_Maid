import random
from telegram import Update
from telegram.ext import ContextTypes

from services.image_fallback import get_kiss_image


KISS_SCENES = [
    "💗 *Maidbot hơi nghiêng người lại gần*\n\n"
    "“Anh này…\n"
    "ở lại thêm chút nữa được không?”",

    "🌸 *Không khí chợt yên lại*\n\n"
    "“Em không nói gì đâu.\n"
    "Chỉ là… em thích khi anh ở gần thế này.”",

    "💞 *Maidbot khẽ mỉm cười*\n\n"
    "“Nếu anh không nói gì,\n"
    "em sẽ coi như anh đồng ý nha…”",

    "✨ *Khoảng cách bỗng ngắn lại*\n\n"
    "“Không cần phải vội.\n"
    "Chỉ một chút thôi… được chứ?”",

    "💓 *Ánh mắt chạm nhau*\n\n"
    "“Anh có nghe tim em đập không?\n"
    "Không phải vì sợ đâu…”",
]


async def kiss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    scene = random.choice(KISS_SCENES)

    image_url = get_kiss_image()

    if image_url:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_url,
            caption=scene,
            parse_mode="Markdown"
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=scene,
            parse_mode="Markdown"
        )
