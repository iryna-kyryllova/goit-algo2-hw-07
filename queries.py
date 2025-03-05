import random
import time


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        return new_node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def move_to_front(self, node):
        if node != self.head:
            self.remove(node)
            node.next = self.head
            if self.head:
                self.head.prev = node
            self.head = node

    def remove_last(self):
        if self.tail:
            last = self.tail
            self.remove(last)
            return last
        return None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.value
        return None

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.key]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node

    def invalidate(self):
        self.cache.clear()
        self.list = DoublyLinkedList()


# Функції без кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


# Функції з LRU-кешем
lru_cache_instance = LRUCache(1000)


def range_sum_with_cache(array, L, R):
    key = (L, R)
    cached_result = lru_cache_instance.get(key)
    if cached_result is not None:
        return cached_result
    result = sum(array[L : R + 1])
    lru_cache_instance.put(key, result)
    return result


def update_with_cache(array, index, value):
    array[index] = value
    keys_to_remove = [
        key for key in lru_cache_instance.cache if key[0] <= index <= key[1]
    ]
    for key in keys_to_remove:
        del lru_cache_instance.cache[key]


# Генерація тестових даних
N = 100_000
Q = 50_000
array = [random.randint(1, 1000) for _ in range(N)]
queries = []
for _ in range(Q):
    if random.random() < 0.7:
        L, R = sorted(random.sample(range(N), 2))
        queries.append(("Range", L, R))
    else:
        index = random.randint(0, N - 1)
        value = random.randint(1, 1000)
        queries.append(("Update", index, value))

# Вимірювання часу виконання без кешу
start_time = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
time_no_cache = time.time() - start_time

# Вимірювання часу виконання з LRU-кешем
start_time = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_with_cache(array, query[1], query[2])
    else:
        update_with_cache(array, query[1], query[2])
time_with_cache = time.time() - start_time

# Виведення результатів
print(f"Час виконання без кешування: {time_no_cache:.2f} секунд")
print(f"Час виконання з LRU-кешем: {time_with_cache:.2f} секунд")
