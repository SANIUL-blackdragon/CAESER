# caeser/redis_client.py

import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True  # So you don't get byte strings
)
