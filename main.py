from atm.controller import ATMController
from atm.bank.fake_bank_api import FakeBankAPI

if __name__ == "__main__":
    bank = FakeBankAPI()
    atm = ATMController(bank_api=bank)

    atm.insert_card("1234-5678-9012-3456")
    atm.enter_pin("4321")
    atm.select_account("checking")

    print("Balance:", atm.get_balance())
    atm.deposit(100)
    print("After deposit:", atm.get_balance())
    atm.withdraw(50)
    print("After withdrawal:", atm.get_balance())
