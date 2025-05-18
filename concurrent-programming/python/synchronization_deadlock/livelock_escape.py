import time
import random
from threading import Thread
from named_lock import NamedLock

# Number of dumplings on the table
DUMPLINGS: int = 20

# Maximum random back‑off (in seconds) before retrying to pick up chopsticks
MAX_BACKOFF = 0.2

class Philosopher(Thread):
    """A philosopher that alternates between thinking and eating dumplings.

    To break the livelock we combine two strategies:
        1.  A global ordering on resources (chopstick names) so that all threads
            always try to acquire the lower‑ranked chopstick first.
        2.  If the second chopstick is not available, release the first, back‑off
            for a random, short period, then start the cycle again.  This avoids
            synchronized give‑and‑take patterns that cause livelock.
    """

    def __init__(self, name: str, left: NamedLock, right: NamedLock):
        super().__init__(name=name)
        # Sort the chopsticks so acquisition order is consistent across threads
        self.first, self.second = sorted([left, right], key=lambda ck: ck.name)

    def run(self) -> None:
        global DUMPLINGS

        while True:
            # Snapshot dumplings under the GIL – quick and safe.
            if DUMPLINGS <= 0:
                break

            acquired_first = self.first.acquire(timeout=MAX_BACKOFF)
            if not acquired_first:
                # Could not get first chopstick; think a bit and retry.
                self.think()
                continue

            # Got the first chopstick – try to get the second without blocking.
            acquired_second = self.second.acquire(blocking=False)
            if not acquired_second:
                # Failed – release first, back‑off randomly, think, and retry.
                self.first.release()
                self.think()
                continue

            # Got both chopsticks – we can eat!
            try:
                if DUMPLINGS <= 0:
                    break
                DUMPLINGS -= 1
                print(f"{self.name} eats a dumpling. Dumplings left: {DUMPLINGS}")
                time.sleep(0.3)  # Simulate the time to eat
            finally:
                # Always release in reverse order
                self.second.release()
                self.first.release()

            # Think for a bit before the next attempt
            self.think()

    def think(self):
        backoff = random.uniform(0.05, MAX_BACKOFF)
        time.sleep(backoff)


if __name__ == "__main__":
    chopstick_a = NamedLock("chopstick_a")
    chopstick_b = NamedLock("chopstick_b")

    philosophers = [
        Philosopher("Philosopher #1", chopstick_a, chopstick_b),
        Philosopher("Philosopher #2", chopstick_b, chopstick_a),
    ]

    for p in philosophers:
        p.start()

    for p in philosophers:
        p.join()

    print("All dumplings are gone – dinner is over!")
