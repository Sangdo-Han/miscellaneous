import time
from threading import Thread
from named_lock import NamedLock

dumplings: int = 20

class Philosopher(Thread):
    def __init__(
        self,
        name: str,
        left_chopstick  : NamedLock,
        right_chopstick : NamedLock 
    ):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick
    
    def run(self):
        global dumplings

        while dumplings > 0:
            self.left_chopstick.acquire()
            print(
                f"{self.left_chopstick.name} grabbed by {self.name}"
            )
            self.right_chopstick.acquire()
            print(
                f"{self.right_chopstick.name} grabbed by {self.name}"
            )
            dumplings -= 1
            print(
                f"{self.name} eats a dumpling"
                f"dumpling left: {dumplings}"
            )
            self.right_chopstick.release()
            print(
                f"{self.right_chopstick.name} released by {self.name}"
            )
            self.left_chopstick.release()
            print(
                f"{self.left_chopstick.name} released by {self.name}"
            )
            print(
                f"{self.name} is thinking ..."
            )
            time.sleep(0.1)

if __name__ == "__main__":
    chopstick_a = NamedLock("chopstick_a")
    chopstick_b = NamedLock("chopstick_b")

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", chopstick_b, chopstick_a)

    ## priority changes -> solves the deadlock
    # philosopher_2 = Philosopher("Philosopher #2", chopstick_a, chopstick_b)

    philosopher_1.start()
    philosopher_2.start()

    philosopher_1.join()
    philosopher_2.join()