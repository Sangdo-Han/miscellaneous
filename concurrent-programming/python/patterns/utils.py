import time

class Timer(object):
    # def __init__(self):
    #     self._start_time = time.perf_counter()
    # def __del__(self):
    #     print(
    #         "Process Ended in "
    #         f"{time.perf_counter()-self._start_time} [s]"
    #     )
    def __enter__(self):
        self._start_time = time.perf_counter()
    def __exit__(self, *exc_info):
        print(
            "Process Ended in "
            f"{time.perf_counter()-self._start_time} [s]"
        )
