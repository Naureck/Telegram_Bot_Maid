import redgifs
from redgifs import Order
import random

def analyze_and_filter_tags():
    api = redgifs.API()
    
    try:
        api.login()
        print("⏳ Đang tải và phân tích dữ liệu Tags...\n")
        
        # Lấy dữ liệu thô (gồm cả name và count)
        all_tags_data = api.get_tags() 
        
        if not all_tags_data:
            print("❌ Không lấy được dữ liệu.")
            return

        # --- BỘ LỌC THÔNG MINH ---
        
        # 1. Nhóm "ĐẠI CHÚNG" (Generic Categories)
        # Điều kiện: Có trên 100.000 video VÀ không phải là subreddit (r/...)
        generic_tags = [
            t['name'] for t in all_tags_data 
            if t['count'] > 100000 and not t['name'].startswith('r/')
        ]
        
        # 2. Nhóm "NGÁCH" (Niche / Specific)
        # Điều kiện: Từ 10.000 đến 100.000 video (Thường là các sở thích cụ thể hơn)
        niche_tags = [
            t['name'] for t in all_tags_data 
            if 10000 < t['count'] <= 100000 and not t['name'].startswith('r/')
        ]

        # 3. Nhóm "DIỄN VIÊN / CÁ NHÂN" (Thường count thấp hơn, hoặc tên riêng)
        # Ở đây ta coi phần còn lại (count < 10.000) là nhóm này
        
        # --- HIỂN THỊ KẾT QUẢ ---
        
        print(f"📊 TỔNG QUAN PHÂN TÍCH ({len(all_tags_data)} tags):")
        print("-" * 50)
        
        print(f"✅ 1. THỂ LOẠI PHỔ BIẾN (Generic) - Tìm thấy: {len(generic_tags)}")
        print(f"   (Dùng cái này cho Menu gợi ý của Bot là đẹp nhất)")
        print(f"   👉 Ví dụ: {random.sample(generic_tags, 10)}")
        print("-" * 30)
        
        print(f"✅ 2. THỂ LOẠI NGÁCH (Niche) - Tìm thấy: {len(niche_tags)}")
        print(f"   👉 Ví dụ: {random.sample(niche_tags, 10)}")
        print("-" * 30)
        
        # In ra danh sách Order luôn để anh tiện theo dõi
        order_list = [o.value for o in Order if not str(o.name).startswith('_')]
        print(f"✅ 3. KIỂU SẮP XẾP (Order): {order_list}")

        return generic_tags, niche_tags

    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        api.close()

if __name__ == "__main__":
    analyze_and_filter_tags()