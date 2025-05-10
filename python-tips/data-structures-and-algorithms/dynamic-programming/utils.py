import time

class Timer:
    def __init__(self):
        self.starttime = None
    def __enter__(self):
        self.starttime = time.perf_counter()
    def __exit__(self, *args, **kwargs):
        print(time.perf_counter() - self.starttime)