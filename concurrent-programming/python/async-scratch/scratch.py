from collections import deque
import time

# 1. "코루틴" 역할을 하는 제너레이터 함수
def my_coroutine(name, delay):
    print(f"Coroutine {name}: 시작!")
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed >= delay:
            print(f"Coroutine {name}: {delay}초 경과, 종료!")
            return  # 코루틴 종료
        print(f"Coroutine {name}: {elapsed:.2f}초 진행...")
        yield # 제어권을 이벤트 루프에 넘김

# 2. 간단한 이벤트 루프
class SimpleEventLoop:
    def __init__(self):
        self.tasks = deque() # 실행 대기 중인 코루틴 (제너레이터) 큐

    def add_task(self, coroutine_generator):
        self.tasks.append(coroutine_generator)

    def run_forever(self):
        while self.tasks:
            current_task = self.tasks.popleft()
            try:
                # 제너레이터를 한 단계 실행 (yield 다음 부분까지)
                next(current_task)
                # 실행 후 다시 큐에 추가 (아직 끝나지 않았으므로)
                self.tasks.append(current_task)
            except StopIteration:
                # 제너레이터가 StopIteration을 발생시키면 종료된 것임
                print(f"Task finished.")
            time.sleep(0.1) # 실제 시스템에서는 I/O 대기 등을 여기서 처리

# 3. Future/Task 객체 (매우 단순화된 버전)
class MyFuture:
    def __init__(self):
        self._result = None
        self._callbacks = []
        self._done = False

    def set_result(self, result):
        if self._done:
            raise RuntimeError("Future already done")
        self._result = result
        self._done = True
        for callback in self._callbacks:
            callback(self)

    def add_done_callback(self, callback):
        if self._done:
            callback(self)
        else:
            self._callbacks.append(callback)

    def result(self):
        if not self._done:
            raise RuntimeError("Future not ready")
        return self._result

    def __iter__(self): # yield from을 흉내낼 때 사용될 수 있음
        # 이터레이터 프로토콜을 구현하여 `yield` 대신 `yield from`처럼 사용될 수 있도록
        # 하지만 순수 제너레이터 기반에서는 직접 `yield`를 사용합니다.
        # 여기서는 단순히 Future를 대기하는 패턴을 보여주기 위함입니다.
        yield self # Future 객체를 yield하여 이벤트 루프에 등록 (실제 구현은 더 복잡)

# 4. 비동기 I/O 흉내내기 (Future와 함께)
def async_io_operation(data, future):
    print(f"  [Simulated I/O]: {data} 처리 시작...")
    def callback():
        time.sleep(2) # 실제 I/O 작업 시간
        future.set_result(f"처리된 데이터: {data} (결과)")
        print(f"  [Simulated I/O]: {data} 처리 완료!")
    # 실제로는 I/O 이벤트 루프(epoll/kqueue)에 등록되어 콜백이 나중에 호출됨
    import threading
    threading.Thread(target=callback).start()


# 코루틴을 Future와 연결하는 함수
def process_data_coroutine(data):
    print(f"코루틴 'ProcessData': 데이터 '{data}' 처리 시작...")
    future = MyFuture()
    async_io_operation(data, future)

    # yield from 대신 직접 Future를 "대기"하는 방식
    # 이 부분은 async/await의 co_await와 유사한 역할을 함
    while not future._done:
        yield # Future가 완료될 때까지 제어권을 넘김
    
    result = future.result()
    print(f"코루틴 'ProcessData': '{data}' 처리 결과: {result}")
    return result

# --- 실행 ---
if __name__ == "__main__":
    print("--- 단순 제너레이터 기반 코루틴 ---")
    loop = SimpleEventLoop()
    loop.add_task(my_coroutine("A", 1.5))
    loop.add_task(my_coroutine("B", 2.0))
    loop.add_task(my_coroutine("C", 1.0))
    loop.run_forever()
    print("--- 단순 제너레이터 기반 코루틴 종료 ---")

    print("\n--- Future와 함께하는 코루틴 ---")
    loop_with_future = SimpleEventLoop()
    loop_with_future.add_task(process_data_coroutine("File1.txt"))
    loop_with_future.add_task(process_data_coroutine("NetworkReq"))
    loop_with_future.add_task(my_coroutine("D", 0.5)) # 다른 코루틴도 섞어서 실행 가능
    loop_with_future.run_forever()
    print("--- Future와 함께하는 코루틴 종료 ---")