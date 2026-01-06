from telegram import Update
from telegram.ext import ContextTypes
from handlers.callback_router import register_callback
from command.nsfw_redgifs import nsfw



async def nsfw_callbacks(update, context):
    query = update.callback_query
    if not query:
        return

    await query.answer()

    if query.data == "nsfw_next":
        await nsfw(update, context)
    elif query.data == "nsfw_save":
        # tạm thời chỉ confirm
        await query.answer("❤️ Đã lưu (chưa implement)")
