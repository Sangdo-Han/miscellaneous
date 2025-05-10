import os
import socket
from threading import Thread
import time

SOCKET_FILE = "./mailBox"

class Sender(Thread):
    def __init__(self):
        super().__init__()
        self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    def run(self):
        self.client.connect(SOCKET_FILE)
        messages = ["Hello World!", " ", "Why so serious?"]
        with self.client:
            for message in messages:
                self.client.sendall(message.encode())

class Receiver(Thread):
    def __init__(self):
        super().__init__()
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    def run(self):
        self.server.bind(SOCKET_FILE)
        self.server.listen()
        conn, addr = self.server.accept()

        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(message)
        
        self.server.close()

def remove_socket():
    if os.path.exists(SOCKET_FILE):
        os.remove(SOCKET_FILE)

def main():
    remove_socket()
    
    receiver : Thread = Receiver()
    sender   : Thread = Sender()

    receiver.start()
    time.sleep(1)
    sender.start()

    receiver.join()
    sender.join()

    remove_socket()

if "__main__" == __name__:
    main()