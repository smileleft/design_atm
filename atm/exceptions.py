class ATMError(Exception):
    """Base class for ATM-related errors."""
    pass


class AuthenticationError(ATMError):
    pass


class AccountNotFoundError(ATMError):
    pass


class InsufficientFundsError(ATMError):
    pass
