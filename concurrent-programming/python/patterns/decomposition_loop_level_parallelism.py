import os
import time
import glob
import typing as T
from multiprocessing.pool import ThreadPool

def search_file(file_location: str, search_string: str) -> bool:
    with open(file_location, 'r', encoding='utf-8') as file:
        return search_string in file.read()

def search_files_concurrently(
        file_locations: T.List[str],
        search_string: str
    ) -> None:
    with ThreadPool() as pool:
        results = pool.starmap(
            search_file,
            (
                (file_location, search_string) for
                file_location in file_locations
            )
        )
        for result, file_name in zip(results, file_locations):
            if result:
                print(f"Found {search_string} was in {file_name}")

if "__main__" == __name__:
    file_locations = list(
        glob.glob(
            "./books/*.txt"
        )
    )
    search_files_concurrently(
        file_locations=file_locations,
        search_string= "brilling"
    )
