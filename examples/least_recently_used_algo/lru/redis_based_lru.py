class RedisLRUCache:
    def __init__(self, redis_client, queue_name, cache_capacity):
        self.redis_client = redis_client
        self.queue_name = queue_name
        self.cache_capacity = cache_capacity

    def clear_cache(self):
        pass

    def add_key(self, key: str):
        pass
