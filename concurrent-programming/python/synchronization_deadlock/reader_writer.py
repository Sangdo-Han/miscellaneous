import time
import random
from threading import Thread
from rwlock import RWLock

counter = 0
RW_LOCK = RWLock()

class User(Thread):
    def __init__(self, idx: int):
        super().__init__()
        self.idx = idx
    
    def run(self) -> None:
        while True:
            RW_LOCK.acquire_read()
            print(f"User - {self.idx} reading : {counter}")
            time.sleep(random.randrange(1,3))
            RW_LOCK.release_read()
            time.sleep(0.5)

class Librarian(Thread):
    def run(self) -> None:
        global counter
        while True:
            RW_LOCK.acquire_write()
            print("Librarian writes ... ")
            counter += 1
            print(f"New value: {counter}")
            time.sleep(random.randrange(1, 3))
            RW_LOCK.release_write()

if "__main__" == __name__:
    threads = [
        User(0),
        User(1),
        Librarian()
    ]

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()