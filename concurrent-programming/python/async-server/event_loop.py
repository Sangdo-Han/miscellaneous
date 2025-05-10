import select
import socket
import typing as T

from collections import deque
from future import Future

Action = T.Callable[[socket.socket, T.Any], Future]
Coroutine = T.Generator[T.Any, T.Any, T.Any]
Mask = int # selectors constant EVENT_READ & EVENT_WRITE

class EventLoop:
    def __init__(self):
        self._num_tasks = 0
        self._ready = deque()
        self._read_waiting : T.Dict[int, T.Tuple[Future, Action]] = {}
        self._write_waiting : dict = {}

    def register_event(
            self, source:socket.socket, event: Mask, future: Future, task: Action
    ) -> None:
        key = source.fileno()
        if event & select.POLLIN:
            self._read_waiting[key] = (future, task)
        elif event & select.POLLOUT:
            self._write_waiting[key] = (future, task)
    
    def add_coroutine(self, task: Coroutine) -> None:
        self._ready.append((task, None))
        self._num_tasks += 1
    
    def add_ready(self, task: Coroutine, msg:T.Optional[str]=None) -> None:
        self._ready.append((task, msg))
    
    def run_coroutine(self, task: Coroutine, msg:T.Optional[str]) -> None:
        try:
            future = task.send(msg)
            future.coroutine(self, task)
        except StopIteration:
            self._num_tasks -= 1
    
    def run_forever(self) -> None:
        while self._num_tasks:
            if not self._ready:
                readers, writers, _ = select.select(
                    self._read_waiting, self._write_waiting, []
                )

                for reader in readers:
                    future, task = self._read_waiting.pop(reader)
                    future.coroutine(self, task)
                
                for writer in writers:
                    future, task = self._write_waiting.pop(writer)
                    future.coroutine(self, task)
                
            task, msg = self._ready.popleft()
            self.run_coroutine(task, msg)
