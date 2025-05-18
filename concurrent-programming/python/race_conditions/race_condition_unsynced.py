import time
import typing as T
from threading import Thread, Lock
from abc import ABC, abstractmethod

class BankAccount(ABC):
    """ Abstract Base Class for bank accounts"""

    # balance: float

    def __init__(self, balance: float = 0):
        self.balance: float = balance

    @abstractmethod
    def deposit(self, amount: float) -> None:
        pass
    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass

class UnsyncedBankAccount(BankAccount):
    def deposit(self, amount: float) -> None:
        if amount > 0:
            temp = self.balance
            self.balance = temp + amount
        else:
            raise ValueError("You cannot deposit negative number")

    def withdraw(self, amount: float) -> None:
        if 0 < amount <= self.balance:
            temp = self.balance
            self.balance = temp - amount
        else:
            raise ValueError("You cannot withdraw negative number")

class SynchedBankAccount(UnsyncedBankAccount):
    def __init__(self, balance = 0):
        super().__init__(balance)
        self.lock = Lock()

    def deposit(self, amount: float) -> None:
        with self.lock:
            super().deposit(amount)

    def withdraw(self, amount: float) -> None:
        with self.lock:
            super().withdraw(amount)

class ATM(Thread):
    def __init__(self, bank_account: BankAccount):
        super().__init__()
        self.bank_account = bank_account

    def transaction(self) -> None:
        time.sleep(0.01)
        self.bank_account.deposit(10)
        self.bank_account.withdraw(10)

    def run(self) -> None:
        self.transaction()

def test_atms(account: BankAccount, num_atms: int = 1000) -> None:
    atms: T.List[ATM] = []
    for _ in range(num_atms):
        atm = ATM(account)
        atms.append(atm)
    
    for atm in atms:
        atm.start()

    for atm in atms:
        atm.join()

if "__main__" == __name__:

    num_atms: int = 1000

    account = UnsyncedBankAccount()
    test_atms(account, num_atms=num_atms)
    print("Balance of unsynced account after concurrent transactinos:")
    print(f"Acutal: {account.balance}\nExpected: 0")

    print("================================")

    account = SynchedBankAccount()
    test_atms(account, num_atms=num_atms)

    print("Balance of synced account after concurrent transactinos:")
    print(f"Acutal: {account.balance}\nExpected: 0")