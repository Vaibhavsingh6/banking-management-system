# Banking Management System

A beginner-friendly command-line Banking Management System made entirely with Python. It supports multiple accounts and stores all information in a local JSON file.

## Features

- Create multiple bank accounts
- Deposit and withdraw money
- Check account balance
- View transaction history
- View all saved accounts
- Input validation and clear error messages
- Persistent JSON storage (`data/accounts.json`)
- Automated tests using Python's built-in `unittest`

## Requirements

- Python 3.10 or later
- No third-party packages are needed

## Run the project

From the project folder, run:

```bash
python main.py
```

Choose an option from the menu. Account numbers must be exactly six digits. The data folder and JSON file are created automatically when data is saved.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
main.py                 # Starts the program
banking/
  cli.py                # Menu and user interaction
  service.py            # Banking rules and validation
  storage.py            # JSON read/write operations
tests/test_service.py   # Automated tests
requirements.txt        # No external dependencies
statement.md            # Project statement
```

## Example flow

1. Create account `123456` for `Asha Sharma` with an opening balance of `1000`.
2. Deposit `500`.
3. Withdraw `200`.
4. Check the balance or open transaction history.

The final balance is `Rs. 1,300.00`, and each money movement appears in the history.

## Data and safety note

This is an educational project, not real banking software. It saves data locally in plain JSON and does not include authentication, encryption, or real-money transfers.
