import random
import requests

from telegram import Update
from telegram.ext import ContextTypes

from services.redgifs_service import get_random_video


# ==============================
# CONFIG
# ==============================

WAIFU_URL = "https://api.waifu.im/search"
GIPHY_URL = "https://api.giphy.com/v1/gifs/search"

GIPHY_API_KEY = "PUT_YOUR_GIPHY_KEY_HERE"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ==============================
# HELPERS
# ==============================

def fetch_maid_image_from_redgifs():
    """
    Chỉ lấy ảnh preview (poster), bỏ video
    """
    try:
        data = get_random_video(["maid"])
        if not data:
            return None

        # Ưu tiên ảnh preview nếu service có trả
        return data.get("poster") or data.get("preview")

    except Exception as e:
        print("RedGifs image error:", e)
        return None


def fetch_maid_from_waifu():
    try:
        params = {
            "included_tags": ["maid"],
            "is_nsfw": False
        }

        r = requests.get(WAIFU_URL, params=params, timeout=10)
        r.raise_for_status()

        images = r.json().get("images", [])
        if not images:
            return None

        return images[0]["url"]

    except Exception as e:
        print("Waifu error:", e)
        return None


def fetch_maid_from_giphy():
    try:
        params = {
            "api_key": GIPHY_API_KEY,
            "q": "anime maid",
            "limit": 10,
            "rating": "g"
        }

        r = requests.get(GIPHY_URL, params=params, timeout=10)
        r.raise_for_status()

        data = r.json().get("data", [])
        if not data:
            return None

        gif = random.choice(data)
        return gif["images"]["original"]["url"]

    except Exception as e:
        print("Giphy error:", e)
        return None


# ==============================
# START HANDLER
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    text = (
        "✨ Chào mừng chủ nhân ✨\n\n"
        "Em là Maidbot 🛎\n"
        "Luôn sẵn sàng mang đến một chút\n"
        "dịu dàng và niềm vui mỗi ngày 💕"
    )

    image_url = None

    # 1️⃣ RedGifs (chỉ ảnh)
    image_url = fetch_maid_image_from_redgifs()

    # 2️⃣ Waifu.im
    if not image_url:
        image_url = fetch_maid_from_waifu()

    # 3️⃣ Giphy (GIF)
    if not image_url:
        image_url = fetch_maid_from_giphy()

    if image_url:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_url,
            caption=text
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text + "\n\n(Em tìm mãi mà hôm nay chưa thấy maid nào 🙈)"
        )
