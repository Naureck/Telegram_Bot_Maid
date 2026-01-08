import random
from telegram import Update
from telegram.ext import ContextTypes

from services.image_fallback import get_cooking_image


COOKING_SCENES = [
    "🍲 *Maidbot đặt bát cơm nóng trước mặt anh*\n\n"
    "“Anh về rồi à~ Em hâm lại đồ ăn rồi đó.\n"
    "Ăn trước cho ấm bụng nha, hôm nay anh mệt rồi.”",

    "🍳 *Trong bếp còn mùi thức ăn ấm*\n\n"
    "“Không có gì cầu kỳ đâu, nhưng là món anh hay thích.\n"
    "Ngồi xuống đi, em múc thêm canh cho.”",

    "🥘 *Maidbot lau tay vào tạp dề, mỉm cười*\n\n"
    "“Hôm nay anh về trễ ha…\n"
    "May là đồ ăn vẫn còn nóng. Ăn xong rồi mình nghỉ ngơi nha.”",

    "🍚 *Bữa cơm giản dị nhưng gọn gàng*\n\n"
    "“Không cần nói gì đâu.\n"
    "Ăn đi… về tới nhà là được rồi.”",

    "🍜 *Hơi nước bốc lên nhẹ nhàng*\n\n"
    "“Em không biết hôm nay anh thế nào,\n"
    "nhưng ít nhất… anh không cần phải ăn một mình.”",
]


async def cooking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    scene = random.choice(COOKING_SCENES)

    image_url = get_cooking_image()

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
