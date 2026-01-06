import requests
import random

WAIFU_API = "https://api.waifu.im/search"

def get_waifu_image():
    try:
        r = requests.get(
            WAIFU_API,
            params={"included_tags": ["maid"]},
            timeout=8
        )
        r.raise_for_status()
        data = r.json()
        images = data.get("images", [])
        if not images:
            return None
        return random.choice(images).get("url")
    except Exception:
        return None
