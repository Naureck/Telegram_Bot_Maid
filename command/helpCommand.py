from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

async def helpCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='''
        /start
        /news - Xem tin tức 📰
        /kiss - Hôn!! 😘
        /cooking - Nấu ăn 🍳
        '''
        )