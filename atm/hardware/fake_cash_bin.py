from atm.interfaces import ICashBin


class FakeCashBin(ICashBin):
    """Fake cash bin for simulation."""

    def __init__(self):
        self.cash_dispensed = 0
        self.cash_received = 0

    def dispense_cash(self, amount: int) -> None:
        self.cash_dispensed += amount

    def accept_cash(self, amount: int) -> None:
        self.cash_received += amount
