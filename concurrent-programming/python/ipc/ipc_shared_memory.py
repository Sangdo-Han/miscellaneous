import time
import threading

SHARED_ARR_SIZE = 5
SHARED_ARR = [-1] * SHARED_ARR_SIZE
lock = threading.Lock()  # Mutex for synchronization

def producer(writing_time: float = 1):
    thread_name = threading.current_thread().name
    for i in range(SHARED_ARR_SIZE):
        time.sleep(writing_time)
        with lock:  # Lock before modifying shared memory
            SHARED_ARR[i] = i
            print(f"{thread_name} writes index {i}: {i}")

def consumer(penalty=1):
    thread_name = threading.current_thread().name
    for i in range(SHARED_ARR_SIZE):
        while True:
            with lock:  # Lock before accessing shared memory
                data = SHARED_ARR[i]
            if data == -1:
                print(f"{thread_name}: No data at index {i}, waiting {penalty} sec")
                time.sleep(penalty)
            else:
                print(f"{thread_name} consumes index {i}, data: {data}")
                break

if __name__ == "__main__":
    consumer_thread = threading.Thread(name="Consumer", target=consumer, args=(1,))
    producer_thread = threading.Thread(name="Producer", target=producer, args=(0.5,))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()