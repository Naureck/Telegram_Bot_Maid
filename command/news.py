from telegram import Update
from telegram.ext import ContextTypes
import requests
from bs4 import BeautifulSoup

def get_News():
    list_news = []
    try:
        # Thêm Header để tránh bị VnExpress chặn vì tưởng là bot (user-agent)
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get('https://vnexpress.net/', headers=headers, timeout=10)
        r.raise_for_status() # Kiểm tra nếu lỗi kết nối
        
        soup = BeautifulSoup(r.text, 'html.parser')
        myDivs = soup.find_all("h3", {"class": "title-news"})

        for new in myDivs:
            if new.a: # Kiểm tra xem thẻ <a> có tồn tại không
                newdict = {}
                link = new.a.get("href")
                # Xử lý nếu link là đường dẫn tương đối
                if link and link.startswith('/'):
                    link = 'https://vnexpress.net' + link
                
                newdict["Link"] = link
                newdict["Title"] = new.a.get("title")
                list_news.append(newdict)
    except Exception as e:
        print(f"Lỗi khi cào tin tức: {e}")
        
    return list_news

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_News()
    if not data:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Xin lỗi Master, con không lấy được tin tức lúc này.")
        return

    max_items = 3
    for index, item in enumerate(data):
        if index >= max_items:
            break
        # Sử dụng f-string với dấu ngoặc đơn bên trong như bạn đã sửa
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"📰 {item['Title']}\n🔗 Link: {item['Link']}"
        )