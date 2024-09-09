from typing import List


class ListLRUCache:
    def __init__(self, cache_capacity):
        self.cache: List[str] = []
        self.cache_capacity = cache_capacity

    def clear_cache(self) -> None:
        try:
            self.cache.clear()
        except:
            print('Error while clearing cache. Retry')
        return None

    def get_key(self, key: str):
        if key in self.cache:
            # since it was accessed move to most recently used
            self.cache.remove(key)
            self.cache.append(key)
            return key
        else:
            return -1

    def add_key(self, key: str):
        if key in self.cache:
            self.cache.remove(key)
        elif len(self.cache) >= self.cache_capacity:
            # remove the least recently used key
            self.cache.pop(0)

        self.cache.append(key)

    def print_cache(self):
        print(f"Current Cache: {self.cache}")
