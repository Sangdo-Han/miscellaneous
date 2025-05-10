import os
import glob
import asyncio

from scheduler import Scheduler
from protocol import Protocol, HOST, PORT, FileWithID

class Server(Protocol):
    def __init__(self, scheduler: Scheduler):
        super.__init__()
        self.scheduler = scheduler
    
    def connection_made(self, transport: asyncio.Transport) -> None:
        peername = transport.get_extra_info("peername")
        print(f"New worker connection from {peername}")
        self.transport = transport
        self.start_new_task()

    def start_new_task(self) -> None:
        command, data = self.scheduler.get_next_task()
        self.send_command(command=command, data=data)
    
    def process_command(self, command, data: FileWithID = None) -> None:
        if command == b"mapdone":
            self.scheduler.map_done(data)
        elif command == b"reducedone":
            self.scheduler.reduce_done()
            self.start_new_task()
        else:
            print(f"Unknown command received {command}")

def main():
    event_loop = asyncio.get_event_loop()
    current_path = os.path.abspath(os.getcwd())
    file_locations = list(
        glob.glob(f"{current_path}/input_files/*.txt")
    )
    scheduler = Scheduler(file_locations)
    server = event_loop.create_server(
        lambda: Server(scheduler), HOST, PORT
    )

    server = event_loop.run_until_complete(server)
    print(f"Serving on {server.sockets[0].getsockname()}")

    try:
        event_loop.run_forever()
    finally:
        server.close()
        event_loop.run_until_complete(server.wait_closed())
        event_loop.close()

if __name__ == "__main__":
    main()