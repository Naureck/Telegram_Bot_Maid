from services.waifu_service import get_waifu_image
from services.giphy_service import get_giphy_gif

def get_start_image():
    return (
        get_waifu_image()
        or get_giphy_gif()
    )
