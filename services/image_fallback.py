import random

from services.waifu_service import get_waifu_image
from services.giphy_service import get_giphy_gif

FALLBACK_IMAGES = [
    "https://i.imgur.com/8Km9tLL.jpg",
    "https://i.imgur.com/zYIlgBl.jpg",
]

def get_start_image():
    return (
        get_waifu_image(tags=["maid", "welcome"])
        or get_giphy_gif()
    )

def get_cooking_image():
    return (
        get_waifu_image(tags=["cooking", "kitchen", "food"])
        or get_giphy_gif(query="anime cooking")
        or get_fallback_image()
    )

def get_kiss_image():
    return (
        get_waifu_image(tags=["romantic", "close-up", "couple"])
        or get_giphy_gif(query="anime romantic")
        or get_fallback_image()
    )

# Fallback image if all else fails
def get_fallback_image():
    return random.choice(FALLBACK_IMAGES)