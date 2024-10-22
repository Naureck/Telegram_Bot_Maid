import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Start Respond
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="What you need, Master?"
        )
    await context.bot.sendPhoto(
            chat_id=update.effective_chat.id,
            photo=open('C:/Users/thr5hr/Pictures/Documents/Temps/maid_daily.jpeg', 'rb'),
            caption="I'm ready for request!"  # Tùy chọn: Chú thích cho hình ảnh
        )

# Help Respond
async def helpCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='''
        /echo - for repeat a message
        /news - for news day
        /kiss - kiss the robot
        /cooking - make some foods
        '''
        )

# News Respond
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

# Kiss Respond
async def kiss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendPhoto(
            chat_id=update.effective_chat.id,
            photo=open('C:/Users/thr5hr/Pictures/Documents/Temps/BlowMaid.jpeg', 'rb'),
            caption="Thank you, Master!"
        )

# Cooking Respond
async def cooking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendPhoto(
            chat_id=update.effective_chat.id,
            photo=open('C:/Users/thr5hr/Pictures/Documents/Temps/CookingMaid.jpeg', 'rb'),
            caption="I'm going to make your meal 🍳"
        )
    await context.bot.sendPhoto(
            chat_id=update.effective_chat.id,
            photo=open('C:/Users/thr5hr/Pictures/Documents/Temps/Meal.png', 'rb'),
            caption="Master, your meal already ❤"
        )

# Echo Respond (repeat)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Unknown Respond
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    # API Tokens
    application = ApplicationBuilder().token('6976477556:AAF9yKOePFO7dtjTZL_JLcjPG_c2RLZRRSo').build()

    # Echo handler
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    # Help handler
    help_handler = CommandHandler('help', helpCommand)
    application.add_handler(help_handler)

    # Start handler
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Kiss handler
    kiss_handler = CommandHandler('kiss', kiss)
    application.add_handler(kiss_handler)

    # Cooking handler
    cooking_handler = CommandHandler('cooking', cooking)
    application.add_handler(cooking_handler)
    
    # News handler
    news_handler = CommandHandler('news', news)
    application.add_handler(news_handler)
    
    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()