import typing as T
from collections import deque
from collections.abc import Generator, AsyncGenerator

Coroutine = T.Generator[None, None, dict]

class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()
    
    def add_coroutine(self, task:Coroutine) -> None:
        self.tasks.append(task)
    
    def run_coroutine(self, task: Coroutine) -> None:
        try:
            task.send(None)
            self.add_coroutine(task)
        except StopIteration:
            print("Task completed")
    
    def run_forever(self) -> None:
        while self.tasks:
            print("Event loop cycle")
            self.run_coroutine(self.tasks.popleft())

def coroutine(name:str, num_yields: int) -> Coroutine:
    for i in range(num_yields):
        print(f"{name}: {i}")
        yield
    
    return i+1

class CoroutineClass:
    def __init__(self, name:str, num_yields: int):
        self.num_yields = num_yields
        self.current = 0
        self.name = name

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.num_yields:
            result = self.current
            print(f"{self.name}: {self.current}")
            self.current += 1
            return result
        else:
            raise StopIteration

    def send(self, *args):
        return self.__next__()

if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(coroutine("Corou #1", num_yields=5))
    event_loop.add_coroutine(coroutine("Corou #2", num_yields=7))
    event_loop.add_coroutine(coroutine("Corou #3", num_yields=6))
    event_loop.add_coroutine(CoroutineClass("Corou #4", num_yields=4))

    event_loop.run_forever()
