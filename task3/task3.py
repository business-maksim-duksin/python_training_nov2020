from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed


class Counter:
    def __init__(self, start=0):
        self.value = start
        self._lock = Lock()

    def increment(self):
        with self._lock:
            self.value += 1

    def __str__(self):
        return str(self.value)


def count(anount, counter):
    for _ in range(anount):
        counter.increment()


def main():
    counter = Counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        pool = [executor.submit(count, 1000000, counter) for _ in range(5)]
        # wait for completion
    # [f for f in as_completed(pool, timeout=2)]
    print("----------------------", counter)  # ???


main()
