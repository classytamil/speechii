import redis
import os
import dotenv

dotenv.load_dotenv()

# --- FOR CLOUD REDIS (RedisLabs / Redis Cloud) ---
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=False,
    decode_responses=True    # return strings instead of bytes
)
