import time
from threading import Thread, Semaphore, Lock
from utils import Timer


SIZE = 5
BUFFER = ["" for _ in range(SIZE)]
producer_idx: int = 0

mutex = Lock()
empty = Semaphore()
full = Semaphore(value=0)

class Producer(Thread):
    def __init__(self, name: str, max_items: int = 5) -> None:
        super().__init__()
        self.counter = 0
        self.name = name
        self.max_itmes = max_items
    
    def next_index(self, index: int) -> int:
        return (index + 1) % SIZE
    
    def run(self) -> None:
        global producer_idx
        while self.counter < self.max_itmes:
            empty.acquire()
            mutex.acquire()
            self.counter += 1
            BUFFER[producer_idx] = f"{self.name} - {self.counter}"
            print(f"{self.name} produced : "
                  f"'{BUFFER[producer_idx]}' into slot {producer_idx}")
            producer_idx = self.next_index(producer_idx)
            mutex.release()
            full.release()
            time.sleep(1)
    
class Consumer(Thread):
    def __init__(self, name: str ,max_items: int = 10):
        super().__init__()
        self.name = name
        self.idx = 0
        self.counter = 0
        self.max_items = max_items
    
    def next_idnex(self) -> int:
        return (self.idx + 1) % SIZE
    
    def run(self) -> None:
        while self.counter < self.max_items:
            full.acquire()
            mutex.acquire()

            item = BUFFER[self.idx]
            print(f"{self.name} consumed item: "
                  f"'{item}' from slot {self.idx}")
            self.idx = self.next_idnex()
            self.counter += 1
            mutex.release()
            empty.release()
            time.sleep(2)

if "__main__" == __name__:
    timer = Timer()
    threads = [
        Producer("SpongeBob"),
        Producer("Patrick"),
        Consumer("Squidward")
    ]

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    