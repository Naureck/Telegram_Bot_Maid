import time
from constants.config import NSFW_CACHE_TTL

def cleanup_nsfw_cache(context):
    cache = context.user_data.get("nsfw_cache", {})
    ts_map = context.user_data.get("nsfw_cache_ts", {})

    now = time.time()
    expired = [
        gid for gid, ts in ts_map.items()
        if now - ts > NSFW_CACHE_TTL
    ]

    for gid in expired:
        cache.pop(gid, None)
        ts_map.pop(gid, None)

    context.user_data["nsfw_cache"] = cache
    context.user_data["nsfw_cache_ts"] = ts_map
