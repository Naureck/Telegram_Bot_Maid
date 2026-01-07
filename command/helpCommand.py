from telegram import Update
from telegram.ext import ContextTypes


async def helpCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛎️ *Maidbot - Trợ lý của Master*\n\n"
        "Em có thể giúp anh với những lệnh sau:\n\n"

        "🚀 */start*\n"
        "– Chào hỏi và giới thiệu nhanh về em\n\n"

        "🔞 */nsfw <tag>*\n"
        "– Tìm nội dung theo chủ đề\n"
        "– Ví dụ: `/nsfw glasses`, `/nsfw cosplay`\n\n"

        "📰 */news*\n"
        "– Xem tin tức mới nhất\n\n"

        "😘 */kiss*\n"
        "– Một nụ hôn động viên tinh thần\n\n"

        "🍳 */cooking*\n"
        "– Gợi ý món ăn và cách nấu\n\n"

        "💡 *Mẹo nhỏ*\n"
        "– Gõ `/nsfw` không kèm gì để xem gợi ý tag\n"
        "– Dùng nút *Next* để xem tiếp, *Save* để lưu lại\n\n"

        "✨ Chúc Master có khoảng thời gian vui vẻ cùng em!"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode="Markdown"
    )
