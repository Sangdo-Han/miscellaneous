import socket
import time

from async_socket import AsyncSocket
from event_loop_with_pool import EventLoop

BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 28080)

class Kitchen:
    @staticmethod
    def cook_pizza(n):
        print(f"Started cooking {n} pizas")
        time.sleep(n)
        print(f"Fresh {n} pizzas are ready!")

class Server:
    def __init__(self, event_loop: EventLoop):
        self.event_loop = event_loop
        print(f"Starting up on : {ADDRESS}")
        self.server_socket = AsyncSocket(socket.create_server(ADDRESS))
    
    def start(self):
        print("Server listening for incoming connections")
        try:
            while True:
                conn, address = yield self.server_socket.accept()
                print(f"Connected to {address}")
                self.event_loop.add_coroutine(
                    self.serve(AsyncSocket(conn))
                )
        except Exception as e:
            self.server_socket.close()
            print("\nServer stopped. {e}")
    
    def serve(self, conn: AsyncSocket):
        while True:
            data = yield conn.recv(BUFFER_SIZE)
            if not data:
                break
            try:
                order = int(data.decode())
                response = f"Thank you for ordering {order} pizzas"
                print(f"Sending message to {conn.getpeername()}")
                yield conn.send(response.encode())

                yield self.event_loop.run_in_executor(
                    Kitchen.cook_pizza, order
                )
                response = f"You order of {order} pizzas is ready! \n"
            
            except ValueError:
                response = "Wrong number of pizzas, please try again! \n"
            
            print(f"Sending message to {conn.getpeername()}")
            yield conn.send(response.encode())
        print(f"Connection with {conn.getpeername()} has been closed")
        conn.close()

if __name__ == "__main__":
    event_loop = EventLoop()
    server = Server(event_loop=event_loop)
    event_loop.add_coroutine(server.start())
    event_loop.run_forever()
