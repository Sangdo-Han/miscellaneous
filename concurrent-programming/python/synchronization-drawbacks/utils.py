import time

class Timer:
    def __init__(self):
        self.starttime = None
    def __enter__(self):
        self.starttime = time.perf_counter()
    def __exit__(self, *args, **kwargs):
        endtime = time.perf_counter()
        lapse = endtime - self.starttime
        print(f"Process Ended in {lapse} [s].")
