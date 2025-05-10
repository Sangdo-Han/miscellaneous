from socket import socket, create_server

class Server:
    def __init__(
        self,
        ip_address:str,
        port:int = 28080,
        buffer_size:int = 1024
    ) -> None:
        self.ip_address = ip_address
        self.port = port
        self.buffer_size = buffer_size
        try:
            self.server_socket = create_server((self.ip_address, self.port))
        except OSError:
            self.server_socket.close()
    
    def accept(self) -> socket:
        conn, client_address = self.server_socket.accept()
        return conn
    
    def serve(self, conn: socket) -> None:
        try:
            while True:
                data = conn.recv(self.buffer_size)
                if not data:
                    break
                try:
                    num_ordered_pizza = int(data.decode())
                    response = f"Thank you for your pizza order {num_ordered_pizza} pizzas"
                except ValueError:
                    response = f"Wrong numbered pizzas, please try again!"
                print(f"Sending message to {conn.getpeername()}")
                conn.send(response.encode())
        except Exception as e:
            print(f"{e}")
        finally:
            print(f"Connection to {conn.getpeername()} has been closed")
            conn.close()

    def start(self)->None:
        print("Server listening for incoming connections")
        try:
            while True:
                conn = self.accept()
                self.serve(conn)
        finally:
            self.server_socket.close()
            print("Server stopped")

if __name__ == "__main__":
    ADDRESS = "127.0.0.1"
    PORT = 28080
    BUFFER_SIZE = 1024 
    server = Server(ip_address=ADDRESS, port=PORT, buffer_size=BUFFER_SIZE)
    server.start()