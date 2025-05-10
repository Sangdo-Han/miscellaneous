import time
from threading import Thread
from named_lock import NamedLock

dumplings : int = 1000

class Philsopher(Thread):
    def __init__(self, name, left_chopstick, right_chopstick):
        super().__init__()

        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick
    
    def run(self) -> None:
        global dumplings

        dumplings_eaten = 0
        while dumplings > 0:
            self.left_chopstick.acquire()
            self.right_chopstick.acquire()
            if dumplings > 0:
                dumplings -= 1
                dumplings_eaten += 1
            time.sleep(1e-4)
            self.right_chopstick.release()
            self.left_chopstick.release()
        print(f"{self.name} took {dumplings_eaten} pieces")

if "__main__" == __name__:
    chopstick_a = NamedLock("chopstick_a")
    chopstick_b = NamedLock("chopstick_b")

    threads = []
    for i in range(10):
        threads.append(
            Philsopher(f"Philosopher #{i}", chopstick_a, chopstick_b)
        )

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()