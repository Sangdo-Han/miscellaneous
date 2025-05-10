import time
import hashlib
import typing as T
from utils import Timer


def get_combinations(len:int, min_num:int=0)->T.List[str]:
    combinations = []
    max_num = 10**len - 1
    for num in range(min_num, max_num):
        str_candidate = str(num).zfill(len)
        combinations.append(str_candidate)
    return combinations

def sha256(str_input:str)->str:
    return hashlib.sha256(str_input.encode()).hexdigest()

def check_hash(hashed_answer:str, assumption:str)->bool:
    return sha256(assumption) == hashed_answer

def crack_password(hashed_answer:str, len:int)->None:
    combinations = get_combinations(len=len)
    for assumption in combinations:
        if check_hash(hashed_answer, assumption):
            print(f"Password Cracked {assumption}")
            break

if __name__ == "__main__":
    answer : int = 8309322
    answer : str = str(answer)
    len : int = 7

    hashed_answer : int = sha256(answer)
    timer = Timer()
    crack_password(hashed_answer, len)
