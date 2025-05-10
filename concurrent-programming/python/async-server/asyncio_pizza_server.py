import asyncio
import socket
import time

ADDRESS = ("127.0.0.1", 28080)
BUFFER_SIZE = 1024

class Kitchen:
    @staticmethod
    def cook_pizza(n):
        print(f"Started cooking {n} pizzas")
        time.sleep(n)
        print(f"Fresh {n} pizzas are ready!")

class Server:
    def __init__(
            self,
            event_loop: asyncio.AbstractEventLoop
    ) -> None:
        self.event_loop = event_loop
        print(f"Starting up at : {ADDRESS}")
        self.server_socket = socket.create_server(ADDRESS)
        self.server_socket.setblocking(False)
    
    async def start(self) -> None:
        print("Server listening for incoming connections")
        try:
            while True:
                conn, client_address = \
                    await self.event_loop.sock_accept(
                        self.server_socket
                    )
                self.event_loop.create_task(
                    self.serve(conn)
                )
        except Exception as e:
            self.server_socket.close()
            print("\nServer stopped.")

    async def serve(self, conn):
        while True:
            data = await self.event_loop.sock_recv(conn, BUFFER_SIZE)
            if not data:
                break
            try:
                order = int(data.decode())
                response = f"Thank you for ordering {order} pizzas! \n"
                print(f"Sending message to {conn.getpeername()}")
                await self.event_loop.sock_sendall(
                    conn, response.encode()
                )
                await self.event_loop.run_in_executor(
                    None, Kitchen.cook_pizza, order
                )
                response = f"Your order of {order} pizzas is ready! \n"
            except ValueError:
                response = f"Wrong number of pizzas, please try again! \n"
            print(f"Sending message to {conn.getpeername()}")
            await self.event_loop.sock_sendall(conn, response.encode())
        print(f"Connection with {conn.getpeername()} has been closed")
        conn.close()

if __name__ == "__main__":
    # will return UnixSelectorEventLoop ( macOS ) 
    event_loop = asyncio.get_event_loop()
    print(event_loop)
    print(type(event_loop))
    server = Server(event_loop=event_loop)
    event_loop.create_task(server.start())
    event_loop.run_forever()