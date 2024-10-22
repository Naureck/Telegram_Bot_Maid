from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes



async def kiss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendPhoto(
            chat_id=update.effective_chat.id,
            photo=open('C:/Users/thr5hr/Pictures/Documents/Temps/BlowMaid.jpeg', 'rb'),
            caption="Thank you, Master!"
        )