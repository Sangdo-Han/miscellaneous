import typing as T
import time
import random
from threading import Thread, Semaphore, Lock

TOTAL_SPOTS = 3

class Garage:
    def __init__(self):
        self.semaphore = Semaphore(TOTAL_SPOTS)
        self.cars_lock = Lock()
        self.parked_cars = []
    def count_parked_cars(self) -> int:
        return len(self.parked_cars)

    def enter(self, car_name: str) -> None:
        self.semaphore.acquire()
        self.cars_lock.acquire()
        self.parked_cars.append(car_name)
        print(f"{car_name} parked")
        self.cars_lock.release()

    def exit(self, car_name: str) -> None:
        self.cars_lock.acquire()
        self.parked_cars.remove(car_name)
        print(f"{car_name} leaving")
        self.semaphore.release()
        self.cars_lock.release()

def park_car(garage:Garage, car_name: str) -> None:
    garage.enter(car_name)
    time.sleep(random.uniform(1,2))
    garage.exit(car_name)

def test_garage(garage:Garage, num_cars:int = 10) -> None:
    threads = []
    for car_num in range(num_cars):
        t = Thread(target=park_car,
                   args= (garage, f"Car #{car_num}"))
        
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

if "__main__" == __name__:
    n_cars = 10
    garage = Garage()
    test_garage(garage, num_cars=n_cars)

