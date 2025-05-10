import time
from queue import Queue
import threading
from threading import Thread
from typing import Callable, Any, Tuple

from utils import Timer

# typedef
Callback = Callable[..., None]
Task = Tuple[Callback, Any, Any]

class Worker(Thread):
    def __init__(self, tasks:Queue[Task]):
        super().__init__()
        self.tasks : Queue = tasks
    
    def run(self):
        while True:
            if not self.tasks.empty():
                func, args, kwargs = self.tasks.get()
                func(*args, **kwargs)
                self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads:int):
        self.tasks = Queue(num_threads)
        self.num_threads = num_threads

        for _ in range(self.num_threads):
            worker = Worker(self.tasks)
            worker.setDaemon(True)
            worker.start()

    def submit(self, func:Callback, *args, **kwargs):
        self.tasks.put((func, args, kwargs))
    
    def wait(self):
        self.tasks.join()

def cpu_waster(idx: int) -> None:
    name = threading.current_thread().getName()
    print(f"{name} : doing {idx} work")
    time.sleep(3)

def main():
    num_jobs     : int   = 20
    num_threads  : int   = 5
    timer        : Timer = Timer()

    pool = ThreadPool(num_threads = num_threads)
    for idx in range(num_jobs):
        pool.submit(cpu_waster, idx)
    pool.wait()

if "__main__" == __name__:
    main()

