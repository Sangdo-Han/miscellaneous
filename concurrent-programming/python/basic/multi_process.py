import os
import time
from multiprocessing import Process

def run_child(cpu_waste_seconds:int) -> None:
    time.sleep(cpu_waste_seconds)
    curr_pid = os.getpid()
    print(f"child ({curr_pid}) : finished job")


def run_parent(num_children:int=3, cpu_waste_seconds:int=2) -> None:
    curr_pid = os.getpid()

    child_processes = [
        Process(target=run_child, args=(cpu_waste_seconds,))
        for _ in range(num_children)
    ]

    for child_process in child_processes:
        child_process.start()

    for child_process in child_processes:
        child_process.join()

    print(f"parent's ({curr_pid}) : finished job")

if __name__ == "__main__":
    num_children       : int = 3
    child_process_time : int = 2
    run_parent(num_children=num_children, cpu_waste_seconds=child_process_time)