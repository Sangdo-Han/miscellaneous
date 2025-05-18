import time
from threading import Thread, Lock

balance : int = 1000

class Consumer(Thread):
    def __init__(self, name, lock):
        super().__init__()

        self.name = name
        self.lock = lock
    
    def run(self) -> None:
        global balance

        spent = 0
        while balance > 0:
            self.lock.acquire()
            if balance > 0:
                balance -= 1
                spent += 1
            time.sleep(1e-4)
            self.lock.release()
        print(f"{self.name} spend {spent} ")

if "__main__" == __name__:
    account = Lock()

    threads = []
    for i in range(10):
        threads.append(
            Consumer(f"Consumer #{i}", account)
        )

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()