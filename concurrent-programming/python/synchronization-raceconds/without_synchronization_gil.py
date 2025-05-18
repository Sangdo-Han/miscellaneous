import time
from threading import Thread

from utils import Timer

GLOBAL_A: int = 0

def increase(num_iterations:int):
    global GLOBAL_A
    for i in range(num_iterations):
        time.sleep(0.00001)
        GLOBAL_A += 1

def main():

    with Timer() as timer:
        num_threads = 4
        num_iterations = 10_000

        threads = [Thread(target=increase, args=(num_iterations, )) for _ in range(num_threads)]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        print(GLOBAL_A)

if __name__ == "__main__":
    main()