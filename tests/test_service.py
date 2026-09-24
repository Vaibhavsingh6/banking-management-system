"""Automated tests for banking rules and JSON persistence."""

import tempfile
import unittest
from pathlib import Path

from banking.service import AccountNotFoundError, BankService, ValidationError
from banking.storage import JSONStorage


class BankServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.service = BankService(JSONStorage(Path(self.temp_dir.name) / "accounts.json"))
        self.service.create_account("123456", "Asha Sharma", 1000)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_deposit_updates_balance_and_persists(self):
        self.assertEqual(self.service.deposit("123456", 250.5), 1250.5)
        self.assertEqual(self.service.get_account("123456")["balance"], 1250.5)

    def test_withdraw_records_transaction(self):
        self.assertEqual(self.service.withdraw("123456", 300), 700)
        account = self.service.get_account("123456")
        self.assertEqual(account["transactions"][-1]["type"], "Withdrawal")

    def test_cannot_withdraw_more_than_balance(self):
        with self.assertRaises(ValidationError):
            self.service.withdraw("123456", 1001)

    def test_duplicate_and_invalid_accounts_are_rejected(self):
        with self.assertRaises(ValidationError):
            self.service.create_account("123456", "Another Name")
        with self.assertRaises(ValidationError):
            self.service.create_account("12", "Asha Sharma")

    def test_missing_account_raises_clear_error(self):
        with self.assertRaises(AccountNotFoundError):
            self.service.get_account("999999")

    def test_blank_data_file_is_initialized(self):
        storage = JSONStorage(Path(self.temp_dir.name) / "blank.json")
        storage.file_path.write_text("\n", encoding="utf-8")

        self.assertEqual(storage.load(), {"accounts": {}})
        self.assertEqual(storage.file_path.read_text(encoding="utf-8"), '{\n  "accounts": {}\n}')


if __name__ == "__main__":
    unittest.main()
