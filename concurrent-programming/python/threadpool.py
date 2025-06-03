import multiprocessing
import queue
import time
import random
from multiprocessing import Process, Event, Queue, current_process
from uuid import uuid4

# 작업자 프로세스
def worker(task_queue: Queue, result_queue: Queue, stop_event: Event):
    while not stop_event.is_set():
        try:
            task = task_queue.get(timeout=0.5)
        except queue.Empty:
            continue
        if task is None:
            continue
        task_id, func, args = task
        print(f"[{current_process().name}] Executing Task {task_id}")
        result = func(*args)
        result_queue.put((task_id, result))

# 예시 작업 함수
def cpu_bound_task(idx):
    print(f"  > Task {idx} started")
    time.sleep(random.uniform(1, 2))
    print(f"  > Task {idx} finished")
    return f"Result of {idx}"

# 지속적으로 관리되는 프로세스 풀 클래스
class PersistentProcessPool:
    def __init__(self, num_workers):
        self.task_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()
        self.stop_event = multiprocessing.Event() # condition variable that can notify all 
        self.workers = [
            Process(target=worker, args=(self.task_queue, self.result_queue, self.stop_event), name=f"Worker-{i}")
            for i in range(num_workers)
        ]
        for p in self.workers:
            p.start()

    def submit(self, func, *args):
        task_id = str(uuid4())
        self.task_queue.put((task_id, func, args))

    def get_result(self):
        try:
            return self.result_queue.get()#(timeout=5)
        except queue.Empty:
            return None

    def shutdown(self):
        self.stop_event.set()
                        # def set(self):
                        #     with self._cond:
                        #         self._flag.acquire(False)
                        #         self._flag.release()
                        #         self._cond.notify_all()
        for p in self.workers:
            p.join()

# 메인 루프: 10개 작업 후 종료
if __name__ == '__main__':
    pool = PersistentProcessPool(num_workers=4)

    try:
        task_count = 10
        completed = 0
        task_index = 0

        # 작업 제출 루프
        while task_index < task_count:
            pool.submit(cpu_bound_task, task_index)
            task_index += 1
            time.sleep(random.uniform(0.5, 1.0))  # 주기적 작업 제출

        # 결과 수집 루프
        while completed < task_count:
            result = pool.get_result()
            if result is not None:
                task_id, output = result
                print(f"[Main] Completed Task {completed + 1}: {output}")
                completed += 1

    finally:
        print("Shutting down pool...")
        pool.shutdown()
