from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import redgifs
import random
from redgifs import Tags
import difflib
from datas.abbreviation import abbreviation_map


api = redgifs.API()
apiTags = Tags()

def get_Nsfw (search_term, order_type):
    list_nsfw = []
    api.login()
    response = api.search(search_term, order=order_type, count=5, page=1)

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
    
    if len(context.args) < 1:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❤Master, Please enter a wanna search text and an order \n\n👉Ex:'/nsfw 3D trending' \n\n📌Order: best, latest, new, oldest, recent, top, top28, trending."
        )
        return

    search_term = context.args[0]
    order_type = getattr(redgifs.Order, context.args[1], redgifs.Order.trending) if len(context.args) > 1 else redgifs.Order.trending
    # getattr(object, attribute_name, default_value)
    #   redgifs.Order là đối tượng chứa các loại sắp xếp như trending, latest, v.v.
    #   user_input[1] là chuỗi mà người dùng nhập vào, ví dụ "trending", "latest", v.v.
    #   redgifs.Order.trending là giá trị mặc định mà bạn muốn trả về nếu người dùng nhập vào một kiểu sắp xếp không hợp lệ.
    
    if search_term in abbreviation_map:
        search_term = abbreviation_map[search_term]

    try:
        data = get_Nsfw(search_term, order_type)
    except redgifs.errors.InvalidTag as e:

        # Lấy danh sách tags từ api
        available_tags = api.get_tags()

        if available_tags:
            # Trích xuất tên thẻ từ danh sách các từ điển
            all_tags = [tag['name'] for tag in available_tags]

            # Tạo danh sách chứa tên các thẻ
            random_tags = random.sample(all_tags, min(20, len(all_tags)))

            # Chuyển danh sách thành chuỗi
            tag_list = f"\n🔹 ".join(random_tags)

            # Nếu không tìm thấy thẻ chính xác, tìm các thẻ gần giống
            similar_tags = difflib.get_close_matches(search_term, all_tags, n=5, cutoff=0.3)

            if similar_tags:
                similar_tags_list = f"\n🔹 ".join(similar_tags)

                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"❌ Tag '{search_term}' is not valid. \n👉Here are some similar tags: \n🔹 {similar_tags_list} \n\n⭕ You can try another tags. \n📋 Some available tags: \n🔹 {tag_list}"
                )
            
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Tag '{search_term}' is not valid and no similar tags found."
                )
            return

    if not data:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No results found for your search."
        )
        return

    for obj in data:
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Here your request \nLink: {obj['Link']} \n(ID: {obj['ID']}) \nAuthor: {obj['Username']} \nCreate date: {obj['CreateDate']} \nTags: {obj['Tags']}"
        )
