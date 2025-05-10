import typing as T
from socket import socket, create_server

class Server:
    def __init__(self, ip_address:str, port:int, buf_size:int = 1024):
        self.clients:T.Set[socket] = set()
        self.ip_address = ip_address
        self.port = port
        self.buf_size = buf_size
        try:
            self.server_socket = create_server((ip_address, port))
            self.server_socket.setblocking(False)
        except OSError as e:
            self.server_socket.close()
            print(f"\nServer Stopped {e}")
    
    def accept(self) -> None:
        try:
            conn, addr = self.server_socket.accept()
            print(f"\nConnected to {addr}")
            conn.setblocking(False)
            self.clients.add(conn)
        except BlockingIOError as e:
            # if you print, while loop continuously detec data is not found 
            # print(f"Server : data not found {e}, contine the server") 
            # [Errno 35] Resource temporarily unavailable.
            # Error handles here // 1
            pass
            # //This exception is caught to
            # handle nonblocking sockets when
            # no data is available to read from
            # the socet. This allows the
            # program to avoid blocking and
            # instead continue execution for
            # other clients with data
            # available to be read
    def serve(self, conn:socket) -> None:
        try:
            while True:
                data = conn.recv(self.buf_size)
                if not data:
                    break
                try:
                    num_pizza_order = int(data.decode())
                    response = f"Thanks for ordering {num_pizza_order} pizzas! \n"

                except ValueError:
                    response = "Wrong number is requested. \n"
                print(f"Sending message to {conn.getpeername()}")
                conn.send(response.encode())
        except BlockingIOError as e:
            # err handles here // 2 
            print(f"Server : data not found {e}, contine the server")
            pass
            # //This exception is caught to
            # handle nonblocking sockets when
            # no data is available to read from
            # the socet. This allows the
            # program to avoid blocking and
            # instead continue execution for
            # other clients with data
            # available to be read
    
    def start(self) -> None:
        print("Server is now listening for incomming connections ... ")
        try:
            while True:
                self.accept()
                for conn in self.clients.copy():
                    self.serve(conn)
        finally:
            self.server_socket.close()
            print("\nServer Closed.")

if __name__ == "__main__":
    server = Server(
        ip_address="127.0.0.1",
        port=28080,
        buf_size=1024
    )
    server.start()
