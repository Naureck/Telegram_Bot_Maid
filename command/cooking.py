from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

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