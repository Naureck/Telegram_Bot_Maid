from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes


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
