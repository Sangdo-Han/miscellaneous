from queue import Queue
from threading import Thread, current_thread
from utils import Timer

class QueueSwaper(Thread):
    def __init__(self, queue_in: Queue, queue_out: Queue, id: int):
        super().__init__(name=str(id))
        self.queue_in = queue_in
        self.queue_out = queue_out

    def run(self) -> None:
        while not self.queue_in.empty():
            item = self.queue_in.get()
            self.queue_out.put(f"Thread-{current_thread}: Data - {item}")


def main(num_items:int, num_threads: int) -> None:
    queue_in = Queue()
    queue_out = Queue()

    for item_number in range(num_items):
        queue_in.put(item_number)

    threads = []

    for thread_idx in range(num_threads):
        thread_ = QueueSwaper(queue_in, queue_out, thread_idx + 1)
        threads.append(thread_)

    for thread_ in threads:
        thread_.start()

    for thread_ in threads:
        thread_.join()

    for item in queue_out.queue:
        print(item)

if "__main__" == __name__:
    num_threads: int   = 2
    num_items: int     = 65545
    timer: Timer       = Timer()
    
    main(num_items, num_threads)
