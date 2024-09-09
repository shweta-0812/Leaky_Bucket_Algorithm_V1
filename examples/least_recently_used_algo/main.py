import os

from lru.list_based_lru import ListLRUCache

CACHE_CAPACITY = 4


def main():
    lru_obj = ListLRUCache(CACHE_CAPACITY)

    insert_pattern = "WXYZZYWX"
    for char in insert_pattern:
        lru_obj.add_key(char)

    lru_obj.print_cache()
    lru_obj.clear_cache()


if __name__ == "__main__":
    main()
