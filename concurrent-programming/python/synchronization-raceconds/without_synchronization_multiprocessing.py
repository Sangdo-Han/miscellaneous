import time
from multiprocessing import Process, Value

from utils import Timer

__GLOBAL_A: int = 0
# Global variable is NOT shared across processes
# Use Value from multiprocessing for shared memory integers

def increase(num_iterations: int, shared_value):
    for _ in range(num_iterations):
        time.sleep(0.00001)
        shared_value.value +=  1

def main():

    with Timer() as timer:
        num_processes = 4
        num_iterations = 10_000
        shared_a = Value('i', 0) # integer type

        processes = [Process(target=increase, args=(num_iterations, shared_a)) for _ in range(num_processes)]
        for process in processes:
            process.start()

        for process in processes:
            process.join()

        print(f"{shared_a.value}")

if __name__ == "__main__":
    main()