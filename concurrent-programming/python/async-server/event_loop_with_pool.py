import select
import socket
import typing as T

from collections import deque
from multiprocessing.pool import ThreadPool
# import multiprocessing as mp
from future import Future

Data = bytes
Action = T.Callable[[socket.socket, T.Any], None]
Mask = int 

BUFFER_SIZE = 1024

class Executor:
    def __init__(self):
        self.pool = ThreadPool()
    
    def execute(self, func, *args):
        future_notify, future_event = socket.socketpair()
        future_event.setblocking(False)

        def _execute():
            result = func(*args)
            future_notify.send(result.encode())
        
        self.pool.apply_async(_execute)
        return future_event

class EventLoop:
    def __init__(self):
        self._num_tasks = 0
        self._ready = deque()
        self._read_waiting = {}
        self._write_waiting = {}
        self.executor = Executor()
    
    def register_event(
            self, source: socket.socket,
            event: Mask, future, task:Action
    ) -> None:
        key = source.fileno()
        if event & select.POLLIN:
            self._read_waiting[key] = (future, task)
        elif event & select.POLLOUT:
            self._write_waiting[key] = (future, task)
    
    def add_coroutine(self, task: T.Generator) -> None:
        self._ready.append((task, None))
        self._num_tasks += 1
    
    def add_ready(self, task: T.Generator, msg: T.Optional[str]=None):
        self._ready.append((task, msg))
    
    def run_coroutine(self, task: T.Generator, msg) -> None:
        try:
            future = task.send(msg)
            future.coroutine(self, task)
        except StopIteration:
            self._num_tasks += 1
    
    def run_in_executor(self, func, *args) -> Future:
        future_event = self.executor.execute(func, *args)
        future = Future()

        def handle_yield(loop: 'EventLoop', task):
            try:
                data = future_event.recv(BUFFER_SIZE)
                loop.add_ready(task, data)
            except BlockingIOError:
                loop.register_event(
                    future_event, select.POLLIN, future, task
                )
        future.set_coroutine(handle_yield)
        return future

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

