import timeit
from functools import lru_cache
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert_node(key, value, self.root)

    def _insert_node(self, key, value, current_node):
        if key < current_node.key:
            if current_node.left:
                self._insert_node(key, value, current_node.left)
            else:
                current_node.left = Node(key, value, current_node)
        elif key > current_node.key:
            if current_node.right:
                self._insert_node(key, value, current_node.right)
            else:
                current_node.right = Node(key, value, current_node)

    def find(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return node.value
        return None

    def _splay(self, node):
        while node.parent:
            if node.parent.parent is None:  # Zig
                if node == node.parent.left:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif (
                node == node.parent.left and node.parent == node.parent.parent.left
            ):  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif (
                node == node.parent.right and node.parent == node.parent.parent.right
            ):  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left
        if left_child is None:
            return
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left:
            node.parent.left = left_child
        else:
            node.parent.right = left_child
        left_child.right = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right
        if right_child is None:
            return
        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    if n < 2:
        return n
    cached_value = tree.find(n)
    if cached_value is not None:
        return cached_value
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


n_values = list(range(0, 951, 50))
lru_times = []
splay_times = []

for n in n_values:
    tree = SplayTree()
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
    lru_times.append(lru_time)
    splay_times.append(splay_time)

# Побудова графіка
plt.figure(figsize=(10, 5))
plt.plot(n_values, lru_times, marker="o", label="LRU Cache")
plt.plot(n_values, splay_times, marker="s", label="Splay Tree")
plt.xlabel("Число Фібоначчі (n)")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
plt.legend()
plt.grid()
plt.show()

# Виведення таблиці
print(f"{'n':<10}{'LRU Cache Time (s)':<22}{'Splay Tree Time (s)':<22}")
print("-" * 54)
for n, lru_time, splay_time in zip(n_values, lru_times, splay_times):
    print(f"{n:<10}{lru_time:<22.8f}{splay_time:<22.8f}")

# ВИСНОВКИ:
# 1. LRU Cache значно ефективніший для великих значень n, оскільки використовує мемоізацію з доступом O(1),
#    що забезпечує швидке повторне використання раніше обчислених значень.
# 2. Splay Tree повільніший, оскільки кожен доступ до збережених значень має складність O(log n),
#    а вставка нових елементів також потребує додаткових обчислень через операції сплаювання.
# 3. Для малих n різниця незначна, але зі збільшенням n затримка у Splay Tree зростає, що видно з графіка.
#
# Отже, LRU Cache є більш ефективним підходом для обчислення чисел Фібоначчі, особливо на великих значеннях n.
