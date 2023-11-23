import os


REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB_NUMBER = int(os.environ.get("REDIS_DB_NUMBER", 1))

BACKEND_CACHE = "redis_cache.cache.RedisCache"


LOCATION_CACHE = "{host}:{port}".format(host=REDIS_HOST, port=REDIS_PORT)


CACHES = {
    "default": {
        "BACKEND": BACKEND_CACHE,
        "LOCATION": LOCATION_CACHE,
        "OPTIONS": {
            "DB": REDIS_DB_NUMBER,
        },
    },
    "esia_raw_data": {
        "BACKEND": BACKEND_CACHE,
        "LOCATION": LOCATION_CACHE,
        "OPTIONS": {
            "DB": 3,
        },
        "TIMEOUT": 60 * 60 * 24 * 3,
    },
}

DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

CACHE_TIMEOUT = 60 * 60 * 24
