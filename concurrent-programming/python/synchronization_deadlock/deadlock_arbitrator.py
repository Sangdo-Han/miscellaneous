import time
from threading import Thread, Lock
from named_lock import NamedLock

dumplings: int = 20

class Waiter:
    def __init__(self):
        self.mutex = Lock()
    
    def ask_for_chopsticks(
            self,
            left_chopstick: NamedLock,
            right_chopstick: NamedLock
    ):
        with self.mutex:
            left_chopstick.acquire()
            print(f"{left_chopstick.name} acquired")
            right_chopstick.acquire()
            print(f"{right_chopstick.name} acquired")
        
    def release_chopsticks(self, left_chopstick: NamedLock,
                           right_chopstick: NamedLock) -> None:
 

        right_chopstick.release()
        print(f"{right_chopstick.name} released ")
        left_chopstick.release()
        print(f"{left_chopstick.name} released\n")
    
class Philosopher(Thread):
    def __init__(self, name: str, waiter: Waiter,
                 left_chopstick: NamedLock,
                 right_chopstick: NamedLock):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick
        self.waiter = waiter

    def run(self) -> None:
        # using globally shared variable
        global dumplings

        while dumplings > 0:
            print(f"{self.name} asks waiter for chopsticks")
            self.waiter.ask_for_chopsticks(
                self.left_chopstick, self.right_chopstick)

            dumplings -= 1
            print(f"{self.name} eats a dumpling. "
                  f"Dumplings left: {dumplings}")
            print(f"{self.name} returns chopsticks to waiter")
            self.waiter.release_chopsticks(
                self.left_chopstick, self.right_chopstick)
            time.sleep(0.1)


if "__main__" == __name__:
    chopstick_a = NamedLock("chopstick_a")
    chopstick_b = NamedLock("chopstick_b")

    waiter = Waiter()

    philosopher_1 = Philosopher("Philosopher #1", waiter, chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", waiter, chopstick_a, chopstick_b)

    philosopher_1.start()
    philosopher_2.start()
    philosopher_1.join()
    philosopher_2.join()
