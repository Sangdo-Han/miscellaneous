import os
import time
import threading
from threading import Thread

def run_sub_thread(idx: int, sleep_time:int=2) -> None:
    sub_thread_name = threading.current_thread().name
    print(
        f"{sub_thread_name} in PID({os.getpid()}) "
        f"is doing {idx} work"
    )
    time.sleep(sleep_time)

def display_threads() -> None:
    print("================")
    print(f"Active threads : {threading.active_count()}")
    for thread_ in threading.enumerate():
        print(thread_)

def main(
    num_threads : int = 5,
    sleep_time  : int = 2    
) -> None:
    display_threads()

    threads = [
        Thread(
            target=run_sub_thread, args=(idx, sleep_time)
        )
        for idx in range(num_threads)
    ]
    
    for thread_ in threads:
        thread_.start()

    display_threads()

    for thread_ in threads:
        thread_.join()

    display_threads() # to check only one thread is available now

if "__main__" == __name__:
    num_threads : int = 5
    main(num_threads)