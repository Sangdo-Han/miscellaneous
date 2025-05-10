import typing as T
from collections import deque
# Coroutine is generator.
Coroutine = T.Generator[None, None, int]

class EventLoop:
    def __init__(self):
        self.tasks : T.Deque[Coroutine] = deque()

    def add_coroutine(self, task:Coroutine) -> None:
        self.tasks.append(task)

    def run_coroutine(self, task:Coroutine) -> None:
        try:
            task.send(None)
            print("result came")
            self.add_coroutine(task)
            print(task)
        except StopIteration: 
            print("Task completed")

    def run_forever(self) -> None:
        while self.tasks:
            print("Event loop cycle")
            self.run_coroutine(self.tasks.popleft())
            print(self.tasks)

def fibonacci(n:int) -> Coroutine:
    a = 0
    b = 1
    for i in range(n):
        temp = a
        a = b
        b = b + temp
        print(f"Fibonacci {i} : {a}")
        yield
    return  a

if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(fibonacci(5))
    event_loop.run_forever()