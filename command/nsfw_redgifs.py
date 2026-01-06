from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from services.redgifs_service import get_random_video


# ==============================
# CONFIG
# ==============================

# Group được phép NSFW (để trống = cho private + mọi group)
ALLOWED_GROUPS = {
    # -100xxxxxxxxxx,
}


# ==============================
# HELPERS
# ==============================

def get_message(update: Update):
    """Lấy message an toàn cho cả command & callback"""
    if update.message:
        return update.message
    if update.callback_query:
        return update.callback_query.message
    return None


def build_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔁 Next", callback_data="nsfw_next"),
            InlineKeyboardButton("❤️ Save", callback_data="nsfw_save"),
        ]
    ])


# ==============================
# MAIN HANDLER
# ==============================

async def nsfw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_message(update)
    if not message:
        return

    if update.callback_query:
        await update.callback_query.answer()

    chat = update.effective_chat

    # --------------------------
    # NSFW GROUP CHECK
    # --------------------------
    if chat.type != "private" and ALLOWED_GROUPS and chat.id not in ALLOWED_GROUPS:
        await message.reply_text("🚫 NSFW không được phép trong group này.")
        return

    # --------------------------
    # PARSE ARGS
    # --------------------------
    if update.message:
        args = [a.lower() for a in context.args]
        context.user_data["nsfw_args"] = args
    else:
        args = context.user_data.get("nsfw_args", [])

    if not args:
        await message.reply_text(
            "Cú pháp:\n"
            "/nsfw <tag> [order] [time]\n\n"
            "Ví dụ:\n"
            "/nsfw milf\n"
            "/nsfw milf top week\n"
            "/nsfw milf cosplay best month"
        )
        return

    orders = {"trending", "latest", "new", "top", "best"}
    times = {"day", "week", "month", "year"}

    order = "trending"
    time_range = "week"
    tags = []

    for arg in args:
        if arg in orders:
            order = arg
        elif arg in times:
            time_range = arg
        else:
            tags.append(arg)

    if update.message:
        await message.reply_text(
            f"🔍 Đang tìm: {' '.join(tags)} | order={order}"
        )

    # --------------------------
    # FETCH FROM SERVICE
    # --------------------------
    try:
        data = get_random_video(tags, order, time_range)


        if not data:
            await message.reply_text("❌ Không tìm thấy kết quả.")
            return
        
        video_url = data["video"]
        author = data["author"]
        gif_tags = ", ".join(data["tags"])

        caption = (
            f"🔥 {author}\n"
            f"🏷 {gif_tags}"
        )

        sent = await context.bot.send_video(
            chat_id=chat.id,
            video=video_url,
            caption=caption,
            reply_markup=build_keyboard()
        )

        file_id = None

        if sent.video:
            file_id = sent.video.file_id

        context.user_data["last_nsfw"] = {
            "type": "video",
            "file_id": file_id,
            "video_url": video_url,
            "caption": caption
        }


    except Exception as e:
        await message.reply_text("⚠️ Lỗi khi truy vấn RedGifs.")
        print("RedGifs error:", e)

    