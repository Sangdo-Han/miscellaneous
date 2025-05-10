# from __future__ import annotations # // to use the higher version content

import typing as T
from collections import deque
from random import randint
import asyncio

Result = T.Any
Burger = Result
Coroutine = T.Callable[[], 'Future']

class Future:
    def __init__(self):
        self.done = None
        self.coroutine = None
        self.result = None
    
    def set_coroutine(self, coroutine: Coroutine) -> None:
        self.coroutine = coroutine
    
    def set_result(self, result: Result) -> None:
        self.done = True
        self.result = result
    
    def __iter__(self) -> 'Future':
        return self
    
    def __next__(self) -> Result:
        if not self.done:
            raise StopIteration
        return self.result
    
class EventLoop:
    def __init__(self) -> None:
        self.tasks = deque()
    
    def add_coroutine(self, coroutine: Coroutine) -> None:
        self.tasks.append(coroutine)
    
    def run_coroutine(self, task: T.Callable[..., 'Future']) -> None:
        future = task()
        future.set_coroutine(task)
        try:
            next(future)
            if not future.done:
                future.set_coroutine(task)
                self.add_coroutine(task)
        except StopIteration:
            return
    
    def run_forever(self) -> None:
        while self.tasks:
            self.run_coroutine(self.tasks.popleft())
    
def cook(on_done: T.Callable[[Burger], None] ) -> None:
    burger = f"Burger #{randint(1,10)}"
    print(f"{burger} is cooked")
    on_done(burger)

def cachier(burger: Burger, on_done: T.Callable[[Burger], None]) -> None:
    print("Burger is ready for pick up!")
    on_done(burger)

def order_burger() -> Future:
    order = Future()

    def on_cachier_done(burger: Burger) -> None:
        print(f"{burger}?!, that's me!")
        order.set_result(burger)

    def on_cook_done(burger: Burger) -> None:
        cachier(burger, on_cachier_done)

    cook(on_cook_done)
    return order

if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(order_burger)
    event_loop.run_forever()