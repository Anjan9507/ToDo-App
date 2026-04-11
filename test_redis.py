from app.core.redis_client import redis_client

redis_client.set("test_key", "Hello Redis")

value = redis_client.get("test_key")

print(value)