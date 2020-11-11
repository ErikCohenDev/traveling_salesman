class HashTableIterator:
    def __init__(self, hash_table):
        self._hash_table = hash_table
        self._index = 0

    def _hash_items_list(self):
        # Big O(n^3)
        hash_items_list = [
            sublist for sublist in self._hash_table._main_list if len(sublist) > 0
        ]
        collision_items = []
        for index, items in enumerate(hash_items_list):
            if len(items) > 1:
                for item in items:
                    collision_items.append([item])
                hash_items_list.remove(hash_items_list[index])
        hash_items_list.extend(collision_items)
        return hash_items_list

    def _hash_size(self):
        # Big O(n^3)
        return len(self._hash_items_list())

    def __next__(self):
        # Big O(n^3)
        if self._index < self._hash_size():
            hash_items_list = self._hash_items_list()
            next_item = hash_items_list[self._index]
            self._index += 1
            return next_item
        else:
            self._index = 0
            raise StopIteration


class HashTable:
    def __init__(self, size=128):
        # Big O(n)
        """Hash Table Class which implements the common functions of setting, getting and modifying data"""
        self._hashtable_size = size
        self._main_list = [[] for j in range(size)]

    def _index(self, key):
        # Big O(n)
        return sum(ord(i) for i in key) % self._hashtable_size

    def __contains__(self, key):
        # Big O(n)
        index = self._index(key)
        return any(dict_key == key for dict_key, dict_value in self._main_list[index])

    def __iter__(self):
        return HashTableIterator(self)

    def set(self, key, value):
        # Big O(1)
        index = self._index(key)
        self._main_list[index].append((key, value))

    __setitem__ = set

    def __getitem__(self, key):
        # Big O(1)
        if key not in self:
            raise KeyError(f"<{key}> not present")
        index = self._index(key)
        for dict_key, value in self._main_list[index]:
            if dict_key == key:
                return value

    def get(self, key, default=None):
        # Big O(1)
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        # Big O(n)
        return list(filter(lambda item: len(item) > 0, self._main_list))

    def __len__(self):
        # Big O(n)
        return sum(len(sublist) for sublist in self._main_list)


def run_tests():
    default_usage()
    nested_hash_table()


def default_usage():
    my_hash_table = HashTable()
    my_hash_table.set("foo", "bar")
    assert my_hash_table.get("foo") == "bar"


def nested_hash_table():
    my_hash_table = HashTable()
    nested_hash_table_instance = HashTable()
    my_hash_table.set("foo", nested_hash_table_instance)
    nested_hash_table_instance.set("alpha", "beta")
    assert nested_hash_table_instance.get("alpha") == "beta"


run_tests()
