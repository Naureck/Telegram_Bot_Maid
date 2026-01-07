import time
import random
import requests
from collections import Counter

REDFIGS_AUTH_URL = "https://api.redgifs.com/v2/auth/temporary"
REDFIGS_SEARCH_URL = "https://api.redgifs.com/v2/gifs/search"

CACHE_TTL = 300  # 5 phút

_TOKEN_CACHE = {
    "token": None,
    "expire": 0
}

_SEARCH_CACHE = {}


_TRENDING_TAG_CACHE = {
    "tags": [],
    "expire": 0
}

# ==============================
# TOKEN
# ==============================

def get_token():
    now = time.time()

    if _TOKEN_CACHE["token"] and now < _TOKEN_CACHE["expire"]:
        return _TOKEN_CACHE["token"]

    r = requests.get(
        REDFIGS_AUTH_URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
        timeout=10
    )
    r.raise_for_status()

    content_type = r.headers.get("Content-Type", "")
    if "application/json" not in content_type:
        raise Exception("RedGifs auth returned non-JSON content")

    token = r.json()["token"]
    _TOKEN_CACHE["token"] = token
    _TOKEN_CACHE["expire"] = now + 50 * 60  # ~50 phút

    return token


# ==============================
# SEARCH
# ==============================

def search(tags, order="trending", time_range="week", limit=20):
    if not tags:
        return []

    cache_key = f"{','.join(tags)}|{order}|{time_range}"
    now = time.time()

    if cache_key in _SEARCH_CACHE:
        ts, data = _SEARCH_CACHE[cache_key]
        if now - ts < CACHE_TTL:
            return data

    token = get_token()  # ❗ DÒNG QUAN TRỌNG NHẤT

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    params = {
        "tags": ",".join(tags),
        "order": order,
        "count": limit
    }

    if order in ("top", "best"):
        params["time"] = time_range

    r = requests.get(
        REDFIGS_SEARCH_URL,
        headers=headers,
        params=params,
        timeout=10
    )
    r.raise_for_status()

    content_type = r.headers.get("Content-Type", "")
    if "application/json" not in content_type:
        raise Exception("RedGifs search returned non-JSON content")

    gifs = r.json().get("gifs", [])
    _SEARCH_CACHE[cache_key] = (now, gifs)

    return gifs


# ==============================
# PUBLIC API
# ==============================

def get_random_video(tags, order="trending", time_range="week"):
    gifs = search(tags, order, time_range)
    if not gifs:
        return None

    gif = random.choice(gifs)
    urls = gif.get("urls", {})

    return {
        "video": urls.get("mp4") or urls.get("sd"),
        "author": gif.get("userName", "unknown"),
        "tags": gif.get("tags", [])[:5],
        "id": gif.get("id"),
    }

# ==============================
# GET TRENDING TAGS
# ==============================
def get_trending_tags(limit=5):
    """
    Lấy top tag trending từ RedGifs (cache 10 phút)
    """
    now = time.time()

    if _TRENDING_TAG_CACHE["tags"] and now < _TRENDING_TAG_CACHE["expire"]:
        return _TRENDING_TAG_CACHE["tags"]

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    params = {
        "order": "trending",
        "count": 50
    }

    r = requests.get(
        REDFIGS_SEARCH_URL,
        headers=headers,
        params=params,
        timeout=10
    )
    r.raise_for_status()

    content_type = r.headers.get("Content-Type", "")
    if "application/json" not in content_type:
        return []

    gifs = r.json().get("gifs", [])

    all_tags = []
    for gif in gifs:
        all_tags.extend(gif.get("tags", []))

    counter = Counter(tag.lower() for tag in all_tags)
    trending = [tag for tag, _ in counter.most_common(limit)]

    _TRENDING_TAG_CACHE["tags"] = trending
    _TRENDING_TAG_CACHE["expire"] = now + 600  # 10 phút

    return trending