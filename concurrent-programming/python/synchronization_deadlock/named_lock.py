import typing as T
from threading import Lock

class NamedLock:
    def __init__(self, name: str):
        self.name = name
        self._lock = Lock()

    def acquire(self):
        self._lock.acquire()
    
    def release(self):
        self._lock.release()
    
    def locked(self) -> bool:
        return self._lock.locked()
    
    def __enter__(self) -> None:
        self.acquire()

    def __exit__(self, *args:T.Tuple[T.Any]) -> None:
        self.release()
