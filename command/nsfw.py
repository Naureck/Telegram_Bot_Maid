from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import redgifs


api = redgifs.API()

def get_Nsfw ():
    list_nsfw = []
    api.login()
    response = api.search('3D', order=redgifs.Order.trending, count=5, page=1)

    for gif in response.gifs:
        newtemp = {}
        newtemp["Link"] = gif.urls.web_url  
        newtemp["CreateDate"] = gif.create_date  
        newtemp["Username"] = gif.username 
        #newtemp["Thumbnail"] = gif.urls.thumbnail
        newtemp["ID"] = gif.id
        newtemp["Tags"] = gif.tags
        list_nsfw.append(newtemp)

    api.close()

    return list_nsfw


async def nsfw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_Nsfw()
    #max_items = 5
    for obj in data:
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Here your request \nLink: {obj['Link']} \n(ID: {obj['ID']}) \nAuthor: {obj['Username']} \nCreate date: {obj['CreateDate']} \nTags: {obj['Tags']}"
        )
