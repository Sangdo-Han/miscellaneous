import time
import threading
from threading import Thread

from multiprocessing import Pipe
from multiprocessing.connection import Connection

from utils import Timer

class WriterThread(object):
    def __init__(self, name:str, conn:Connection, data:list=[]):
        self.conn = conn
        self.data = data
        self._thread = Thread(
            target=self.do_thread_job,
            name=name,
        )

    def start(self):
        self._thread.start()

    def join(self):
        self._thread.join()

    def do_thread_job(self):
        print(f"{self._thread.name} thread: {threading.current_thread()}")
        time.sleep(1)
        self.conn.send(self.data)

class ReceiverThread(object):
    def __init__(self, name:str, conn: Connection):
        self.conn = conn
        self._thread = Thread(
            target=self.do_thread_job,
            name=name
        )

    def start(self):
        self._thread.start()

    def join(self):
        self._thread.join()

    def do_thread_job(self):
        print(f"{self._thread.name} thread: {threading.current_thread()}")
        messages = self.conn.recv()
        print(messages)

def main():
    timer = Timer()
    conn1, conn2 = Pipe()

    writer_thread = WriterThread(
        name="writer",
        conn=conn1,
        data=["Hello World!", "why so serious"]
    )
    receiver_thread = ReceiverThread(
        name="receiver",
        conn=conn2
    )

    threads = [writer_thread, receiver_thread]
    for thread_ in threads:
        thread_.start()
    
    for thread_ in threads:
        thread_.join()

if "__main__" == __name__:
    main()