import socket

from async_socket import AsyncSocket
from event_loop import EventLoop

BUFFER_SIZE = 1024 
ADDRESS = ("127.0.0.1", 28080)

class Server:
    def __init__(self, event_loop:EventLoop):
        self.event_loop = event_loop
        self.server_socket = AsyncSocket(
            socket=socket.create_server(ADDRESS)
        )
    
    def start(self):
        print("Server listening for incoming connections")
        try:
            while True:
                conn, address = yield self.server_socket.accept()
                print(f"Connected to {address}")
                self.event_loop.add_coroutine(
                    self.serve(AsyncSocket(conn))
                )
        except Exception:
            self.server_socket.close()
            print("\nServer stopped")
    
    def serve(self, conn: AsyncSocket):
        while True:
            data = yield conn.recv(BUFFER_SIZE)
            if not data:
                break

            try:
                order = int(data.decode())
                response = f"Thank you for ordering {order} pizzas!\n"
            except ValueError:
                response = f"Wrong number of pizza, please try again\n"
            
            print(f"Sending message to {conn.getpeername()}")
            yield conn.send(response.encode())
        print(f"Connection with {conn.getpeername()} has been closed")
        conn.close()

if __name__ == "__main__":
    event_loop = EventLoop()
    server = Server(event_loop=event_loop)
    event_loop.add_coroutine(server.start())
    event_loop.run_forever()