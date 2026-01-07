import time
import random
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.redgifs_service import get_random_video, get_trending_tags


# ==============================
# CONFIG
# ==============================

# Group được phép NSFW (trống = private + mọi group)
ALLOWED_GROUPS = {
    # -100xxxxxxxxxx,
}

# Global cache tag
POPULAR_TAGS_DYNAMIC = set()
MAX_TAGS = 50  # số lượng tag hiển thị tối đa

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


def update_popular_tags(gifs):
    """Cập nhật danh sách tag phổ biến toàn cầu"""
    global POPULAR_TAGS_DYNAMIC
    for gif in gifs:
        for tag in gif.get("tags", []):
            POPULAR_TAGS_DYNAMIC.add(tag.lower())
    # Giữ tối đa MAX_TAGS tag
    if len(POPULAR_TAGS_DYNAMIC) > MAX_TAGS:
        POPULAR_TAGS_DYNAMIC = set(list(POPULAR_TAGS_DYNAMIC)[-MAX_TAGS:])


def build_keyboard(tags=None):
    """Tạo inline keyboard với tag suggestion + Next/Save"""
    buttons = []
    if tags:
        for tag in tags:
            buttons.append([InlineKeyboardButton(tag, callback_data=f"nsfw_tag_{tag.lower()}")])

    # Always add Next/Save buttons
    buttons.append([
        InlineKeyboardButton("🔁 Next", callback_data="nsfw_next"),
        InlineKeyboardButton("❤️ Save", callback_data="nsfw_save"),
    ])

    return InlineKeyboardMarkup(buttons)


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

    # Nếu không args, show tag suggestion
    if not args:
        # 1. lấy tag trending
        trending_tags = get_trending_tags(limit=5)

        # 2. fallback nếu API lỗi
        if not trending_tags:
            trending_tags = ["milf", "cosplay", "blonde", "hentai", "asian"]

        buttons = [
            [InlineKeyboardButton(tag.upper(), callback_data=f"nsfw_tag_{tag}")]
            for tag in trending_tags
        ]

        await message.reply_text(
            "🔥 Tag đang hot trên RedGifs:",
            reply_markup=InlineKeyboardMarkup(buttons)
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
        await message.reply_text(f"🔍 Đang tìm: {' '.join(tags)} | order={order}")

    # --------------------------
    # SAVE USER SEARCH HISTORY
    # --------------------------
    searched_tags = context.user_data.get("searched_tags", [])
    for tag in tags:
        if tag not in searched_tags:
            searched_tags.insert(0, tag)  # tag mới lên đầu
    context.user_data["searched_tags"] = searched_tags[:MAX_TAGS]  # giới hạn số lượng

    # --------------------------
    # FETCH FROM SERVICE
    # --------------------------
    try:
        data = get_random_video(tags, order, time_range)

        if not data:
            await message.reply_text("❌ Không tìm thấy kết quả.")
            return

        # Cập nhật tag global cache
        update_popular_tags([data])

        video_url = data["video"]
        author = data["author"]
        gif_id = data["id"]
        gif_tags = ", ".join(data["tags"])
        tags = data["tags"][:5]

        caption = (
            f"ℹ️ {author}\n"
            f"🏷 {gif_tags}\n"
        )

        sent = await context.bot.send_video(
            chat_id=chat.id,
            video=video_url,
            caption=caption,
            reply_markup=build_keyboard()
        )

        # Lưu user_data để Next/Save (nếu cần)
        context.user_data["last_nsfw"] = {
            "type": "video",
            "video_url": video_url,
            "caption": caption,
            "tags": tags,
            "id": gif_id,
            "author": data.get("author", "unknown"),
            "source": f"https://www.redgifs.com/watch/{gif_id}"
        }

    except Exception as e:
        await message.reply_text("⚠️ Lỗi khi truy vấn RedGifs.")
        print("RedGifs error:", e)
