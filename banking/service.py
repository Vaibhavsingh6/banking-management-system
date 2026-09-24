"""Business rules for the Banking Management System."""

from datetime import datetime


class BankError(Exception):
    """Base exception for expected banking errors."""


class ValidationError(BankError):
    """Raised for invalid user input."""


class AccountNotFoundError(BankError):
    """Raised when an account number does not exist."""


class BankService:
    """Manage accounts using a storage object with load and save methods."""

    def __init__(self, storage):
        self.storage = storage

    @staticmethod
    def _clean_account_number(account_number):
        account_number = str(account_number).strip()
        if not account_number.isdigit() or len(account_number) != 6:
            raise ValidationError("Account number must contain exactly 6 digits.")
        return account_number

    @staticmethod
    def _clean_name(name):
        name = str(name).strip()
        if len(name) < 2 or not all(character.isalpha() or character.isspace() for character in name):
            raise ValidationError("Name must contain at least 2 letters and spaces only.")
        return " ".join(name.split())

    @staticmethod
    def _amount(amount):
        try:
            amount = float(amount)
        except (TypeError, ValueError) as error:
            raise ValidationError("Amount must be a valid number.") from error
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return round(amount, 2)

    @staticmethod
    def _transaction(transaction_type, amount, balance):
        return {
            "type": transaction_type,
            "amount": amount,
            "balance_after": balance,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def _account(self, account_number, data):
        account_number = self._clean_account_number(account_number)
        try:
            return account_number, data["accounts"][account_number]
        except KeyError as error:
            raise AccountNotFoundError("No account was found with that number.") from error

    def create_account(self, account_number, name, opening_balance=0):
        account_number = self._clean_account_number(account_number)
        name = self._clean_name(name)
        try:
            opening_balance = float(opening_balance)
        except (TypeError, ValueError) as error:
            raise ValidationError("Opening balance must be a valid number.") from error
        if opening_balance < 0:
            raise ValidationError("Opening balance cannot be negative.")
        opening_balance = round(opening_balance, 2)

        data = self.storage.load()
        if account_number in data["accounts"]:
            raise ValidationError("An account with that number already exists.")
        account = {"name": name, "balance": opening_balance, "transactions": []}
        if opening_balance > 0:
            account["transactions"].append(
                self._transaction("Opening balance", opening_balance, opening_balance)
            )
        data["accounts"][account_number] = account
        self.storage.save(data)
        return account

    def deposit(self, account_number, amount):
        amount = self._amount(amount)
        data = self.storage.load()
        _, account = self._account(account_number, data)
        account["balance"] = round(account["balance"] + amount, 2)
        account["transactions"].append(self._transaction("Deposit", amount, account["balance"]))
        self.storage.save(data)
        return account["balance"]

    def withdraw(self, account_number, amount):
        amount = self._amount(amount)
        data = self.storage.load()
        _, account = self._account(account_number, data)
        if amount > account["balance"]:
            raise ValidationError("Insufficient balance for this withdrawal.")
        account["balance"] = round(account["balance"] - amount, 2)
        account["transactions"].append(self._transaction("Withdrawal", amount, account["balance"]))
        self.storage.save(data)
        return account["balance"]

    def get_account(self, account_number):
        data = self.storage.load()
        _, account = self._account(account_number, data)
        return account.copy()

    def list_accounts(self):
        data = self.storage.load()
        return [(number, account.copy()) for number, account in data["accounts"].items()]
