import typing as T

class Future:
    def __init__(self):
        self.coroutine = None
    def set_coroutine(self, coroutine: T.Callable):
        self.coroutine = coroutine
    