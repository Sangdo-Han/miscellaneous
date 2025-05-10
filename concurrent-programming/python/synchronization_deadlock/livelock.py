import time
from threading import Thread
from named_lock import NamedLock

dumplings: int = 20

class Philosopher(Thread):
    def __init__(self, name:str, left_chopstick:NamedLock, right_chopstick:NamedLock):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        global dumplings

        while dumplings > 0:
            self.left_chopstick.acquire()

            print(
                f"{self.left_chopstick.name} chopstick"
                f"grabbed by {self.name}"
            )

            if self.right_chopstick.locked():
                print(
                    f"{self.name} cannot get the "
                    f"{self.right_chopstick.name} chopstick, "
                    "politely concededs ..."
                )
            else:
                self.right_chopstick.acquire()
                print(
                    f"{self.right_chopstick.name} chopstick "
                    f"grabbed by {self.name}"
                )
                dumplings -= 1
                print(
                    f"{self.name} eats a dumpling. "
                    f"Dumplings left: {dumplings}"
                )
                time.sleep(1)
                self.right_chopstick.release()

            self.left_chopstick.release()

if "__main__" == __name__:
    chopstick_a = NamedLock("chopstick_a")
    chopstick_b = NamedLock("chopstick_b")

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()

    # philosopher_1.join()
    # philosopher_2.join()
