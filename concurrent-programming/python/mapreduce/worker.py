import os
import re
import json
import asyncio
import typing as T
from uuid import uuid4

from protocol import Protocol, HOST, PORT, FileWithID, Occurence

ENCODING = "ISO-8859-1"
RESULT_FILENAME = "result.json"

class Worker(Protocol):

    def connection_lost(self, exc):
        print("The server closed the connection")
        asyncio.get_running_loop().stop()
    
    def process_command(self, command, data):
        if command == b"map":
            self.handle_map_request(data)
        elif command == b"reduce":
            self.handle_reduce_request(data)
        elif command == b"disconnect":
            self.connection_lost(None)
        else:
            print(f"Unknown command received : {command}")
    def mapfn(self, filename: str):
        word_counts = {}
        with open(filename, "r", encoding=ENCODING) as f:
            for line in f:
                words = re.split("\W+", line)
                for word in words:
                    word = word.lower()
                    if word != "":
                        if word not in word_counts:
                            word_counts[word] = []
                        word_counts[word].append(1)
        return word_counts

    def combinefn(self, results) -> Occurence:
        combined_results = {}
        for key in results.keys():
            combined_results[key] = sum(results[key])
        return combined_results
    
    def reducefn(self, map_files) -> Occurence:
        reduced_results = {}
        for filename in map_files.values():
            with open(filename, "r") as f:
                d = json.load(f)
                for k, v in d.items():
                    reduced_results[k] = v + reduced_results.get(k,0)
        return reduced_results
    
    def handle_map_request(self, map_file:FileWithID):
        temp_results = self.mapfn(map_file[1])
        results = self.combinefn(temp_results)
        temp_file = self.save_map_results(results)
        self.send_command(
            command = b"mapdone", data=(map_file[0], temp_file)
        )

    def save_map_result(self, results: Occurence) -> str:
        temp_dir = self.get_temp_dir()
        temp_file =os.path.join(temp_dir, f"{uuid4()}.json")
        with open(temp_file, "w") as f:
            d = json.dumps(results)
            f.write(d)
        return temp_file
    
    def handle_reduce_request(self, data:T.Dict[str, str]) -> None:
        results = self.reducefn(data)
        with open(RESULT_FILENAME, "W") as f:
            d = json.dumps(results)
            f.write(d)
        self.send_command(
            command=b"reducedone",
            data=("0", RESULT_FILENAME)
        )

def main():
    event_loop = asyncio.get_event_loop()
    coroutine = event_loop.create_connection(Worker, HOST, PORT)
    event_loop.run_until_complete(coroutine)
    event_loop.run_forever()
    event_loop.close()

if __name__ == "__main__":
    main()
