from redgifs import Tags
import redgifs

# Khởi tạo API và đăng nhập
api = redgifs.API()
api.login()

# Tạo đối tượng Tags
apiTags = Tags()

# Tải danh sách các thẻ vào tags_mapping
all_tags = api.get_tags()

# Kiểm tra xem có thẻ nào không
if all_tags:
    print("All tags loaded successfully.")

    apiTags.tags_mapping = {tag['name']: tag['name'] for tag in all_tags}

    # Gọi random() để lấy ngẫu nhiên một thẻ
    random_tag = apiTags.random(count=5)
    print(f"Random Tag: {random_tag}")
else:
    print("No tags found.")