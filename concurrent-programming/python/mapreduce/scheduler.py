import asyncio
from enum import Enum
import typing as T

from protocol import FileWithID

class State(Enum):
    START = 0
    MAPPING = 1
    REDUCING = 2
    FINISHED = 3

class Scheduler:
    def __init__(self, file_locations: T.List[str]):
        self.state = State.START
        self.data_len = len(file_locations)
        self.file_locations : T.Iterator = iter(enumerate(file_locations))
        self.working_maps : T.Dict[str, str] = {}
        self.map_results : T.Dict[str, str] = {}
    
    def get_next_task(self) -> T.Tuple[bytes, T.Any]:
        if self.state == State.START:
            print("STARTED")
            self.state = State.MAPPING
        
        if self.state == State.MAPPING:
            try:
                map_item = next(self.file_locations)
                self.working_maps[map_item[0]] = map_item[1]
                return b"map", map_item
            except StopIteration:
                if len(self.working_maps) > 0:
                    return b"disconnect", None
                self.state = State.REDUCING
        
        if self.state == State.REDUCING:
            return b"reduce", self.map_results
        
        if self.state == State.FINISHED:
            print("FINISHED")
            asyncio.get_running_loop().stop()
            return b"disconnect", None
    
    def map_done(self, data: FileWithID):
        if not data[0] in self.working_maps:
            return
        
        self.map_results[data[0]] = data[1]
        del self.working_maps[data[0]]
        print(f"MAPPING {len(self.map_results)} / {self.data_len}")
    
    def reduce_done(self):
        print("REDUCING 1/1")
        self.state = State.FINISHED

