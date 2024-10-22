from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup


def get_News():
    list_news=[]
    r = requests.get('https://vnexpress.net/')
    soup = BeautifulSoup(r.text, 'html.parser') # r.text là html của trang

    myDivs = soup.find_all("h3", {"class": "title-news"})

    for new in myDivs:
        newdict = {}
        newdict["Link"] = new.a.get("href")
        newdict["Title"] = new.a.get("title")
        list_news.append(newdict)
    return list_news

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_News()
    max_items = 3
    for index, item in enumerate(data):
        if index >= max_items:
            break
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Latest News \n {item["Link"]}"
            )