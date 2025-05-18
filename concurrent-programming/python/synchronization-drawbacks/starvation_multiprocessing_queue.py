import time
import multiprocessing as mp

class Consumer(mp.Process):
    def __init__(self, name, task_queue: mp.Queue, result_queue: mp.Queue):
        super().__init__()
        self.name = name
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        spent = 0
        while True:
            if self.task_queue.empty():
                continue # 시작 대기 
            else:
                item = self.task_queue.get(block=True)
                if item is None:
                    break # 종료 신호
                spent += 1

        self.result_queue.put({self.name: spent})
        print(f"{self.name} spend {spent} ")

if "__main__" == __name__:
    num_consumers = 10
    total_tasks = 1000
    task_queue = mp.Queue()
    result_queue = mp.Queue()

    # 작업 Queue에 작업 추가
    for _ in range(total_tasks):
        task_queue.put(1) # 작업 내용을 명시할 수도 있습니다. 여기서는 단순히 소비 횟수를 세므로 1을 넣습니다.

    # 종료 신호 추가 1000 + 10
    for _ in range(num_consumers):
        task_queue.put(None)

    consumers = []
    for i in range(num_consumers):
        consumer = Consumer(f"Consumer #{i}", task_queue, result_queue)
        consumers.append(consumer)

    for consumer in consumers:
        consumer.start()

    for consumer in consumers:
        consumer.join()

    # gathering from queue become empty
    results = {}
    while not result_queue.empty():
        results.update(result_queue.get())

    total_spent = sum(results.values())
    print(f"\nTotal spent: {total_spent}")
