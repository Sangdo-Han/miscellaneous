import os
import json
import asyncio
import typing as T

FileWithID = T.Tuple[str, str]
Occurence = T.Tuple[str, int]

PORT = 28080
HOST = "127.0.0.1"
TEMP_DIR = "temp"
END_MESSAGE = b"EOF"

class Protocol(asyncio.Protocol):
    def __init__(self):
        super.__init__()
        self.buffer = b""
    
    def connection_made(self, transport: asyncio.Trasnport):
        self.transport = transport
    
    def data_received(self, data: bytes):
        self.buffer += data
        if END_MESSAGE in self.buffer:
            if b":" not in data:
                command, _ = self.buffer.split(END_MESSAGE, 1)
                data = None
            else:
                command, data = self.buffer.split(b":", 1)
                data, self.buffer = data.split(END_MESSAGE, 1)
                data = json.loads(data.decode())
            self.process_command(command, data)
    
    def send_command(self, command, data: FileWithID = None):
        if data:
            pdata = json.dumps(data).encode()
            self.transport.write(command + b":" + pdata + END_MESSAGE)
        else:
            self.transport.write(command + END_MESSAGE)
    
    def get_temp_dir(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, TEMP_DIR)

    def process_command(self, command: bytes, data):
        raise NotImplementedError
