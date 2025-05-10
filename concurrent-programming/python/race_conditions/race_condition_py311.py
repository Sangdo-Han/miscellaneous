import time
import threading
from threading import Lock
from utils import Timer

class UnsynchedBankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        temp = self.balance
        time.sleep(1e-6)  # Artificial delay
        self.balance = temp + amount

    def withdraw(self, amount):
        temp = self.balance
        time.sleep(1e-6)
        self.balance = temp - amount

class SynchedBankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.mutex = Lock()

    def deposit(self, amount):
        with self.mutex: 
            temp = self.balance
            time.sleep(1e-6)
            self.balance = temp + amount

    def withdraw(self, amount):
        with self.mutex:
            temp = self.balance
            time.sleep(1e-6)
            self.balance = temp - amount

def atm_transaction(account):
    for _ in range(100):
        account.deposit(1)
        account.withdraw(1)

if __name__ == "__main__":
    # account = UnsynchedBankAccount()
    account = SynchedBankAccount()
    threads = [
        threading.Thread(
            target=atm_transaction, args=(account,)
        ) for _ in range(1000)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Final Balance: {account.balance} (Expected: 0)")
