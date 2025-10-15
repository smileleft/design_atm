from atm.interfaces import IBankAPI


class FakeBankAPI(IBankAPI):
    """Fake in-memory bank system for testing."""

    def __init__(self):
        self._pins = {"1234-5678-9012-3456": "4321"}
        self._accounts = {
            "1234-5678-9012-3456": {
                "checking": 100,
                "savings": 500,
            }
        }

    def verify_pin(self, card_number: str, pin: str) -> bool:
        return self._pins.get(card_number) == pin

    def get_accounts(self, card_number: str):
        return self._accounts.get(card_number, {})

    def update_balance(self, account_id: str, new_balance: int) -> None:
        for _, accounts in self._accounts.items():
            if account_id in accounts:
                accounts[account_id] = new_balance
                return
        raise ValueError("Account not found")
