# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
import random
import threading
from queue import Queue


class BaseCrawler:
    def __init__(self, max_workers: int = 3, num_consumers: int = 2):
        self._buffer = Queue()
        self._num_consumers = num_consumers
        self._max_workers = max_workers
        self._lock = threading.Lock()
        self._completed = False

    def _producer(self):
        for _ in range(100):
            item = random.randint(1, 100)
            print(f"写入: {item}")
            self._buffer.put(item)
        self._producer_end()

    def _producer_end(self):
        with self._lock:
            self._completed = True

    def _consumer(self):
        while True:
            try:
                with self._lock:
                    if self._completed and self._buffer.empty():
                        break

                if not self._buffer.empty():
                    item = self._buffer.get()
                    self._process_data(item)
                    self._buffer.task_done()
            except (BaseException, Exception):
                pass

    @staticmethod
    def _process_data(item):
        print(f'读取: {item}')

    def before(self):
        pass

    def after(self):
        pass

    def start(self):
        self.before()
        with ThreadPoolExecutor(max_workers=self._max_workers) as pool:
            pool.submit(self._producer)
            for _ in range(self._num_consumers):
                pool.submit(self._consumer)
        self._buffer.join()
        self.after()


if __name__ == "__main__":
    crawler = BaseCrawler()
    crawler.start()
