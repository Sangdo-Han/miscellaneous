from __future__ import annotations

import select
import socket
import typing as T

from future import Future
from event_loop import EventLoop

Data = bytes

class AsyncSocket:
    def __init__(self, socket: socket.socket):
        self._socket = socket
        self._socket.setblocking(False)
    
    def recv(
            self,
            bufsize : int
    ) -> None:
        future = Future()

        def handle_yield(loop: EventLoop, task) -> None:
            try:
                data = self._socket.recv(bufsize)
                loop.add_ready(task, data)
            except BlockingIOError:
                loop.register_event(self._socket, select.POLLIN, future, task)
        
        future.set_coroutine(handle_yield)
        return future
    
    def send(
            self,
            data: Data
    ) -> Future:
        future = Future()

        def handle_yield(loop: EventLoop, task):
            try:
                sent_num = self._socket.send(data)
                loop.add_ready(task, sent_num)
            except BlockingIOError:
                loop.register_event(self._socket, select.POLLOUT, future, task)
        
        future.set_coroutine(handle_yield)
        return future

    def accept(self) -> Future:
        future = Future()

        def handle_yield(loop, task):
            try:
                soc, addr = self._socket.accept()
                loop.add_ready(task, (soc, addr))
            except BlockingIOError:
                loop.register_event(self._socket, select.POLLIN, future, task)
        future.set_coroutine(handle_yield)
        return future
    
    def close(self) -> Future:
        future = Future()
        def handle_yield(*_):
            self._socket.close()
        
        future.set_coroutine(handle_yield)
        return future
    
    def __getattr__(self, name:str) -> T.Any:
        return getattr(self._socket, name)
