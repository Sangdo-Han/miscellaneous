import multiprocessing as mp
import random
import time

class BankAccount:
    def __init__(self, account_name:str, initial_balance:int):
        self.account_name = account_name
        self.balance = mp.Manager().Value('i', initial_balance)
        self.lock = mp.Lock()

class Bank:
    @staticmethod
    def transfer_deadlock_prone(src_account: BankAccount, dest_account: BankAccount, amount:int) -> None:
        with src_account.lock:
            time.sleep(random.uniform(0.1, 0.3))
            with dest_account.lock:
                if src_account.balance >= amount:
                    src_account.balance -= amount
                    dest_account.balance += amount
                else:
                    print(f"{src_account.name} has no money.")

    @staticmethod
    def transfer_without_deadlock(src_account: BankAccount, dest_account:BankAccount, amount:int) -> None:
        lk_dict = {
            src_account.account_name : src_account.lock,
            dest_account.account_name: dest_account.lock
        }
        lk_nested = sorted(lk_dict.items(), key=lambda x: x[0])
        with lk_nested[0][1]:
            time.sleep(random.uniform(0.1, 0.3))
            with lk_nested[1][1]:
                if src_account.balance.value >= amount:
                    src_account.balance.value -= amount
                    dest_account.balance.value += amount
                else:
                    print(f"{src_account.name} has no money.")


if __name__ == "__main__":

    san_account = BankAccount("san", 100)
    han_account = BankAccount("han", 50)

    print(f"SAN Account: {san_account.balance.value}, HAN Account: {han_account.balance.value}")

    p1 = mp.Process(
        target=Bank.transfer_without_deadlock,
        args=(san_account, han_account, 50)
    )
    p2 = mp.Process(
        target=Bank.transfer_without_deadlock,
        args=(han_account, san_account, 30)
    )

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"SAN Account: {san_account.balance.value}, HAN Account: {han_account.balance.value}")


    # p1 = mp.Process(target=Bank.transfer_deadlock_prone, args=(san_account, han_account, 50))
    # p2 = mp.Process(target=Bank.transfer_deadlock_prone, args=(han_account, san_account, 30))
    # p1.start()
    # p2.start()
    # p1.join(timeout=3)
    # p2.join(timeout=3)
    # if p1.is_alive():
    #     print("프로세스 1: 교착 상태 발생 가능성 또는 시간 초과")
    #     p1.terminate()
    # if p2.is_alive():
    #     print("프로세스 2: 교착 상태 발생 가능성 또는 시간 초과")
    #     p2.terminate()
    # print(f"SAN Account: {san_account.balance.value}, HAN Account: {han_account.balance.value}")

