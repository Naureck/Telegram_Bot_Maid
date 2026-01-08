from telegram import Update
from telegram.ext import ContextTypes
import requests
from bs4 import BeautifulSoup
import time

from services.image_fallback import get_fallback_image

VNEXPRESS_URL = "https://vnexpress.net/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

EMOJIS = ["🔥", "💭", "🚆", "📌", "📰"]

# cache ảnh bài viết (tránh spam request)
_IMAGE_CACHE = {}
IMAGE_CACHE_TTL = 600  # 10 phút


# ==============================
# FETCH NEWS LIST
# ==============================

def fetch_news(limit: int = 3):
    results = []

    try:
        r = requests.get(VNEXPRESS_URL, headers=HEADERS, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.find_all("h3", class_="title-news", limit=15)

        for item in items:
            if len(results) >= limit:
                break

            a = item.find("a")
            if not a:
                continue

            title = a.get("title")
            link = a.get("href")

            if not title or not link:
                continue

            if link.startswith("/"):
                link = VNEXPRESS_URL.rstrip("/") + link

            results.append({
                "title": title.strip(),
                "link": link.strip()
            })

    except Exception as e:
        print("NEWS FETCH ERROR:", e)

    return results


# ==============================
# FETCH ARTICLE IMAGE
# ==============================

def fetch_article_image(url: str):
    now = time.time()

    # dùng cache nếu còn hạn
    if url in _IMAGE_CACHE:
        img_url, ts = _IMAGE_CACHE[url]
        if now - ts < IMAGE_CACHE_TTL:
            return img_url
        else:
            _IMAGE_CACHE.pop(url, None)

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        meta = soup.find("meta", property="og:image")

        if meta and meta.get("content"):
            img = meta["content"]
            _IMAGE_CACHE[url] = (img, now)
            return img

    except Exception as e:
        print("IMAGE FETCH ERROR:", e)

    fallback = get_fallback_image()
    _IMAGE_CACHE[url] = (fallback, now)
    return fallback


# ==============================
# /NEWS HANDLER
# ==============================

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    news_list = fetch_news(limit=3)

    if not news_list:
        await context.bot.send_message(
            chat_id=chat_id,
            text="😔 Hôm nay em chưa lấy được tin tức rồi Master..."
        )
        return
    
    # thời gian hiện tại
    now = time.gmtime(time.time() + 7 * 3600) # UTC+7
    time_str = time.strftime("%d/%m/%Y", now)

    # lời dẫn mở đầu
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "🛎️ *Maidbot điểm tin cho Master nè~*\n"
            f"🕘 `{time_str}`"
        ),
        parse_mode="Markdown"
    )

    # gửi từng tin kèm ảnh
    for idx, item in enumerate(news_list):
        emoji = EMOJIS[idx % len(EMOJIS)]
        image_url = fetch_article_image(item["link"])

        caption = (
            f"{emoji} *{item['title']}*\n"
            f"🔗 {item['link']}"
        )

        try:
            if image_url:
                try:
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=image_url,
                        caption=caption,
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print("PHOTO FAILED, FALLBACK TO TEXT:", e)
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=caption,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=caption,
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )
        except Exception as e:
            print("NEWS SEND ERROR:", e)
