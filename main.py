import os
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Command
from command.start import start
from command.news import news
from command.helpCommand import helpCommand
from command.kiss import kiss
from command.cooking import cooking
from command.nsfw import nsfw

load_dotenv()
botToken = os.getenv("TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Echo Respond (repeat)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Unknown Respond
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    # API Tokens
    application = ApplicationBuilder().token(botToken).build()

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

    # NSFW handler
    nsfw_handler = CommandHandler('nsfw', nsfw)
    application.add_handler(nsfw_handler)
    
    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()