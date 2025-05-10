from socket import socket, create_server
from threading import Thread

class Handler(Thread):
    def __init__(self, conn:socket, buffer_size:int):
        super().__init__()
        self.conn = conn
        self.buffer_size = buffer_size
    
    def run(self)->None:
        print(f"Connected to {self.conn.getpeername()}")
        try:
            while True:
                data = self.conn.recv(self.buffer_size)
                if not data:
                    break
                try:
                    num_pizza_order = int(data.decode())
                    response = f"Thank you for ordering {num_pizza_order} pizzas.\n"
                except ValueError:
                    response = "Wrong Number of pizza, please try again.\n"
                print(f"Sending Message to {self.conn.getpeername()}")
                self.conn.send(response.encode())
        except Exception as e:
            print(f"{e}")
        finally:
            print(f"Connection to {self.conn.getpeername()} has been closed\n")
            self.conn.close()

class Server:
    def __init__(self, ip_address="127.0.0.1", port=28080):
        try:
            print(f"Start Server {ip_address}, {port}")
            self.server_socekt = create_server((ip_address, port))
        except OSError:
            self.server_socekt.close()
            print("Server stopped")

    def start(self) -> None:
        print(f"Server listening for incomming connection")
        try:
            while True:
                conn, address = self.server_socekt.accept()
                print(f"Client connection requested from {address}")
                thread = Handler(conn, buffer_size=1024)
                thread.start()
        finally:
            thread.join()
            self.server_socekt.close()
            print(f"Server Stopped")

if __name__ == "__main__":
    server = Server()
    server.start()