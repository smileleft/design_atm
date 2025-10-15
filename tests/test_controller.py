import pytest
from atm.controller import ATMController
from atm.bank.fake_bank_api import FakeBankAPI
from atm.hardware.fake_card_reader import FakeCardReader
from atm.hardware.fake_cash_bin import FakeCashBin
from atm.exceptions import AuthenticationError, InsufficientFundsError


@pytest.fixture
def atm():
    bank = FakeBankAPI()
    card_reader = FakeCardReader("1234-5678-9012-3456")
    cash_bin = FakeCashBin()
    return ATMController(bank_api=bank, card_reader=card_reader, cash_bin=cash_bin)


def test_atm_full_flow(atm):
    assert atm.insert_card() == "Card 1234-5678-9012-3456 inserted."
    assert atm.enter_pin("4321") is True
    assert "checking" in atm.bank_api.get_accounts("1234-5678-9012-3456")

    msg = atm.select_account("checking")
    assert "checking" in msg
    assert atm.get_balance() == 100

    # Deposit
    new_balance = atm.deposit(50)
    assert new_balance == 150
    assert atm.cash_bin.cash_received == 50

    # Withdraw
    new_balance = atm.withdraw(20)
    assert new_balance == 130
    assert atm.cash_bin.cash_dispensed == 20

    # Eject
    assert atm.eject_card() == "Card ejected."


def test_wrong_pin(atm):
    atm.insert_card()
    with pytest.raises(AuthenticationError):
        atm.enter_pin("9999")


def test_insufficient_funds(atm):
    atm.insert_card()
    atm.enter_pin("4321")
    atm.select_account("checking")
    with pytest.raises(InsufficientFundsError):
        atm.withdraw(999)
