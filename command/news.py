from telegram import Update
from telegram.ext import ContextTypes
import requests
from bs4 import BeautifulSoup


VNEXPRESS_URL = "https://vnexpress.net/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ==============================
# FETCH NEWS
# ==============================

def fetch_news(limit: int = 3):
    news_list = []

    try:
        r = requests.get(
            VNEXPRESS_URL,
            headers=HEADERS,
            timeout=10
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.find_all("h3", class_="title-news")

        for item in items:
            if len(news_list) >= limit:
                break

            a_tag = item.find("a")
            if not a_tag:
                continue

            title = a_tag.get("title")
            link = a_tag.get("href")

            if not title or not link:
                continue

            if link.startswith("/"):
                link = VNEXPRESS_URL.rstrip("/") + link

            news_list.append({
                "title": title.strip(),
                "link": link
            })

    except Exception as e:
        print("NEWS ERROR:", e)

    return news_list


# ==============================
# /NEWS HANDLER
# ==============================

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    news_list = fetch_news(limit=3)

    if not news_list:
        await context.bot.send_message(
            chat_id=chat_id,
            text="😔 Xin lỗi Master, em không lấy được tin tức lúc này."
        )
        return

    lines = ["📰 *Tin tức mới nhất từ VnExpress*\n"]

    for idx, item in enumerate(news_list, start=1):
        lines.append(
            f"{idx}. *{item['title']}*\n"
            f"🔗 {item['link']}\n"
        )

    text = "\n".join(lines)

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
