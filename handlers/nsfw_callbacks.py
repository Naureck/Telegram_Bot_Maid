import time
import os

from telegram import Update
from telegram.ext import ContextTypes
from handlers.callback_router import register_callback
from command.nsfw_redgifs import nsfw

NEXT_COOLDOWN = 1.5  # giây


async def nsfw_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return


    if query.data.startswith("nsfw_tag_"):
        tag = query.data.replace("nsfw_tag_", "").strip()

        if not tag:
            await query.answer("⚠️ Tag không hợp lệ rồi Master!", show_alert=True)
            return

        context.user_data["nsfw_args"] = [tag]
        await nsfw(update, context)

    elif query.data == "nsfw_next":
        args = context.user_data.get("nsfw_args")

        if not args:
            await query.answer(
                "⚠️ Hãy chọn tag hoặc dùng /nsfw <tag> trước nha",
                show_alert=True
            )
            return

        now = time.time()
        last_ts = context.user_data.get("last_nsfw_next_ts", 0)

        if now - last_ts < NEXT_COOLDOWN:
            await query.answer(
                "⏳ Từ từ thôi... Em đang lấy nội dung mới",
                show_alert=False
            )
            return

        context.user_data["last_nsfw_next_ts"] = now

        await nsfw(update, context)


    elif query.data == "nsfw_save":
        data = context.user_data.get("last_nsfw")

        SAVE_CHANNEL_ID = int(os.getenv("SAVE_CHANNEL_ID", "0"))

        if SAVE_CHANNEL_ID == 0:
            await query.answer(
                "⚠️ Chưa cấu hình kênh lưu",
                show_alert=True
            )
            return

        if not data:
            await query.answer(
                "⚠️ Chưa có nội dung để lưu, thưa Master!",
                show_alert=True
            )
            return
        
        # Lưu ID đã lưu vào user_data để tránh lưu trùng
        saved_ids = context.user_data.get("saved_nsfw_ids", set())

        if data["id"] in saved_ids:
            await query.answer(
                "⚠️ Video này đã được lưu rồi nha Master!",
                show_alert=True
            )
            return
        
        # Lây ID người dùng
        #user_id = update.effective_user.id 

        try:
            tags = data["tags"]
            gif_id = data["id"]
            short_link = f"redgifs.com/{gif_id}"

            hashtags = " ".join(f"#{t.replace(' ', '').lower()}"for t in tags)

            author = data.get("author", "unknown")
            source = short_link
            
            caption_lines = [hashtags]

            if author != "unknown":
                caption_lines.append(f"🎬 Created by @{author}")

            if source:
                caption_lines.append(f"🔗 Source: {source}")

            caption = "\n".join(caption_lines)

            await context.bot.send_video(
                chat_id=SAVE_CHANNEL_ID,
                video=data["video_url"],
                caption=caption
            )
            
            # Cập nhật danh sách ID đã lưu
            saved_ids.add(data["id"])
            context.user_data["saved_nsfw_ids"] = saved_ids

            await query.answer("❤️ Em đã lưu rồi nha!", show_alert=True)

        except Exception as e:
            await query.answer(
                "❌ Lưu thất bại rồi Master!",
                show_alert=True
            )
            print("SAVE ERROR:", e)

