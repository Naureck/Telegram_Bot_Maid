import requests
import random
import os

GIPHY_API = "https://api.giphy.com/v1/gifs/search"

def get_giphy_gif(query="anime maid"):
    try:
        params = {
            "api_key": os.getenv("GIPHY_KEY"),
            "q": query,
            "limit": 10,
            "rating": "pg-13"
        }
        r = requests.get(GIPHY_API, params=params, timeout=8)
        r.raise_for_status()
        data = r.json().get("data", [])
        if not data:
            return None
        return random.choice(data)["images"]["original"]["url"]
    except Exception:
        return None
