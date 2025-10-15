class Account:
    def __init__(self, account_id: str, balance: int = 0):
        self.account_id = account_id
        self.balance = balance


class Card:
    def __init__(self, card_number: str):
        self.card_number = card_number
