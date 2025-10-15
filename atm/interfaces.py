from abc import ABC, abstractmethod
from typing import Dict


class IBankAPI(ABC):
    """Abstract interface for future real bank system integration."""

    @abstractmethod
    def verify_pin(self, card_number: str, pin: str) -> bool:
        pass

    @abstractmethod
    def get_accounts(self, card_number: str) -> Dict[str, int]:
        pass

    @abstractmethod
    def update_balance(self, account_id: str, new_balance: int) -> None:
        pass


class ICardReader(ABC):
    """Abstract interface for ATM card reader."""

    @abstractmethod
    def read_card(self) -> str:
        pass


class ICashBin(ABC):
    """Abstract interface for cash deposit and withdrawal."""

    @abstractmethod
    def dispense_cash(self, amount: int) -> None:
        pass

    @abstractmethod
    def accept_cash(self, amount: int) -> None:
        pass
