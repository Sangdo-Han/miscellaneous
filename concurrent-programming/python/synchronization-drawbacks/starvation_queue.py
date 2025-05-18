import time
from threading import Thread
from queue import Queue

class Consumer(Thread):
    def __init__(self, name, task_queue:Queue, result_queue:Queue):
        super().__init__()

        self.name = name
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self) -> None:
        spent = 0
        while True:
            if self.task_queue.empty():
                continue # 시작 대기 
            else:
                item = self.task_queue.get(block=True)
                if item is None:
                    break # 종료 신호
                spent += 1

        print(f"{self.name} spend {spent} ")

if "__main__" == __name__:
    num_consumers = 10
    total_tasks = 1000
    task_queue = Queue()
    result_queue = Queue()

    for _ in range(total_tasks):
        task_queue.put(1)
    
    for _ in range(num_consumers):
        task_queue.put(None)

    results = {}

    threads = []
    for i in range(10):
        threads.append(
            Consumer(f"Consumer #{i}", task_queue, result_queue)
        )

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    

    # gathering from queue become empty
    results = {}
    while not result_queue.empty():
        results.update(result_queue.get())

    total_spent = sum(results.values())
    print(f"\nTotal spent: {total_spent}")