from typing import Optional
from atm.models import Account, Card
from atm.interfaces import IBankAPI, ICardReader, ICashBin
from atm.exceptions import AuthenticationError, AccountNotFoundError, InsufficientFundsError


class ATMController:
    """Main ATM controller — manages the full flow."""

    def __init__(self, bank_api: IBankAPI,
                 card_reader: Optional[ICardReader] = None,
                 cash_bin: Optional[ICashBin] = None):
        self.bank_api = bank_api
        self.card_reader = card_reader
        self.cash_bin = cash_bin

        self.current_card: Optional[Card] = None
        self.authenticated = False
        self.current_account: Optional[Account] = None

    def insert_card(self, card_number: Optional[str] = None):
        """Simulate card insertion."""
        if self.card_reader and not card_number:
            card_number = self.card_reader.read_card()
        if not card_number:
            raise ValueError("Card number required")

        self.current_card = Card(card_number)
        self.authenticated = False
        self.current_account = None
        return f"Card {card_number} inserted."

    def enter_pin(self, pin: str) -> bool:
        if not self.current_card:
            raise AuthenticationError("No card inserted.")
        is_valid = self.bank_api.verify_pin(self.current_card.card_number, pin)
        self.authenticated = is_valid
        if not is_valid:
            raise AuthenticationError("Invalid PIN.")
        return True

    def select_account(self, account_id: str):
        if not self.authenticated:
            raise AuthenticationError("PIN not verified.")
        accounts = self.bank_api.get_accounts(self.current_card.card_number)
        if account_id not in accounts:
            raise AccountNotFoundError(f"Account '{account_id}' not found.")
        self.current_account = Account(account_id, accounts[account_id])
        return f"Account '{account_id}' selected with balance ${self.current_account.balance}"

    def get_balance(self) -> int:
        if not self.current_account:
            raise AccountNotFoundError("No account selected.")
        return self.current_account.balance

    def deposit(self, amount: int) -> int:
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if not self.current_account:
            raise AccountNotFoundError("No account selected.")

        self.current_account.balance += amount
        self.bank_api.update_balance(self.current_account.account_id, self.current_account.balance)
        if self.cash_bin:
            self.cash_bin.accept_cash(amount)
        return self.current_account.balance

    def withdraw(self, amount: int) -> int:
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if not self.current_account:
            raise AccountNotFoundError("No account selected.")
        if self.current_account.balance < amount:
            raise InsufficientFundsError("Insufficient funds.")

        self.current_account.balance -= amount
        self.bank_api.update_balance(self.current_account.account_id, self.current_account.balance)
        if self.cash_bin:
            self.cash_bin.dispense_cash(amount)
        return self.current_account.balance

    def eject_card(self):
        self.current_card = None
        self.authenticated = False
        self.current_account = None
        return "Card ejected."
