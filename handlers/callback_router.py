import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

CALLBACK_MAP = {}

def register_callback(key):
    def decorator(func):
        CALLBACK_MAP[key] = func
        return func
    return decorator


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return

    await query.answer()

    handler = CALLBACK_MAP.get(query.data)

    if not handler:
        logger.warning(f"Unknown callback: {query.data}")
        return

    await handler(update, context)
