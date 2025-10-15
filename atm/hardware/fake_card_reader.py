from atm.interfaces import ICardReader


class FakeCardReader(ICardReader):
    """Fake card reader for testing."""

    def __init__(self, card_number: str):
        self.card_number = card_number

    def read_card(self) -> str:
        return self.card_number
