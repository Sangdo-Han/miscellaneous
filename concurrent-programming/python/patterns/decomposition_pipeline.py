import time
import threading
from queue import Queue
import typing as T
from utils import Timer

Workload = T.AnyStr

class SharedCounter:
    def __init__(self, initial_value:int = 0):
        self._value = initial_value
        self._mutex = threading.Lock()
    def increment(self):
        with self._mutex:
            self._value += 1
    def decrement(self):
        with self._mutex:
            self._value -= 1
    def get(self):
        with self._mutex:
            return self._value

class Worker(threading.Thread):
    def __init__(
        self,
        in_queue: Queue[Workload],
        out_queue: T.Optional[Queue[Workload]],
        job_type: str,
        turnaround_time: int = 4,
        num_projects: int = 4,  # Ensure workers know the number of projects
        process_counter: T.Optional[SharedCounter] = None
    ):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.job_type = job_type
        self.turnaround_time = turnaround_time
        self.num_projects = num_projects
        if process_counter:
            self.process_counter = process_counter
        else:
            self.process_counter = SharedCounter(initial_value=0)

    def run(self) -> None:
        while self.process_counter.get() < self.num_projects:
            try:
                workload = self.in_queue.get(timeout=1)  # Avoid infinite blocking
            except Exception:
                continue  # Keep checking if no task available

            if workload is None:
                self.in_queue.task_done()
                break  # Stop if sentinel received

            print(f"{self.job_type} .... {workload}")
            time.sleep(self.turnaround_time)
            self.process_counter.increment()

            if self.out_queue:
                self.out_queue.put(workload)

            self.in_queue.task_done()

class Pipeline:
    def __init__(self, num_projects: int = 4):
        self.num_projects = num_projects

    def assemble_leathers(self) -> Queue[Workload]:
        projects_in: Queue[Workload] = Queue()
        for idx in range(self.num_projects):
            projects_in.put(f"Shoes #{idx}")
        return projects_in

    def run_concurrently(self) -> None:
        to_be_planned = self.assemble_leathers()
        to_be_programmed = Queue()
        to_be_finalized = Queue()

        designer = Worker(to_be_planned, to_be_programmed, "Designer", turnaround_time=0.2, num_projects=self.num_projects)

        # Assume that data decomposition. we hired multiple manufacturers.
        shared_counter = SharedCounter(initial_value=0) # use as an atomic value in C++
        # suppose that manufacturer1 is more skillful than manufacturer2 
        manufacturer1 = Worker(to_be_programmed, to_be_finalized, "Manufacturer 1", turnaround_time=0.4, num_projects=self.num_projects, process_counter=shared_counter)
        manufacturer2 = Worker(to_be_programmed, to_be_finalized, "Manufacturer 2", turnaround_time=0.5, num_projects=self.num_projects, process_counter=shared_counter)

        manager = Worker(to_be_finalized, None, "Manager", turnaround_time=0.1, num_projects=self.num_projects)

        designer.start()
        manufacturer1.start()
        manufacturer2.start()
        manager.start()

        # Wait for all tasks to be processed
        designer.join()
        manufacturer1.join()
        manufacturer2.join()
        manager.join()


if __name__ == "__main__":
    with Timer() as timer:
        pipeline = Pipeline(num_projects=100)
        pipeline.run_concurrently()
