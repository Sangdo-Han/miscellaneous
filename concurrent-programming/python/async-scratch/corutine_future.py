import random
import time
import typing as T

from collections import deque

Result = T.Any
Coroutine = T.Callable[[], 'Future']

class Future:
    def __init__(self) -> None:
        self._is_done = False
        self._coroutine = None
        self._result = None

    def set_coroutine(self, coroutine: Coroutine) -> None:
        self._coroutine = coroutine
    
    def set_result(self, result:Result) -> None:
        self._is_done = True
        self._result = result
    
    def __iter__(self) -> "Future":
        return self
    
    def __next__(self) -> Result:
        if not self._is_done:
            raise StopIteration
        return self._result
    
    @property
    def is_done(self):
        return self._is_done

class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()
    
    def add_coroutine(self, coroutine: Coroutine) -> None:
        self.tasks.append(coroutine)
    
    def run_coroutine(self, task: T.Callable[..., Future]) -> None:
        future = task() # Coroutine 의 generator 객체 자체가 future
        future.set_coroutine(task)
        try:
            next(future)
            if not future.is_done:
                