import time
import multiprocessing as mp

balance : int = 1000

class Consumer(mp.Process):
    def __init__(self, name, lock:mp.Lock, shared_value:mp.Value):
        super().__init__()
        self.name = name
        self.lock = lock
        self.shared_value = shared_value

    def run(self):
        spent = 0
        while self.shared_value.value > 0:
            with self.lock:
                if self.shared_value.value > 0:
                    self.shared_value.value -= 1
                    spent += 1
                time.sleep(1e-4)
        print(f"{self.name} spend {spent} ")

if "__main__" == __name__:
    account = mp.Lock()
    balance = mp.Value('i', 1000)

    processes = []
    for i in range(10):
        processes.append(
            Consumer(f"Consumer #{i}", account, balance)
        )

    for t in processes:
        t.start()
    
    for t in processes:
        t.join()