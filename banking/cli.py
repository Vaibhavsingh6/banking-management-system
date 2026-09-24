"""Interactive menu for the Banking Management System."""

from banking.service import BankError, BankService
from banking.storage import JSONStorage, StorageError


def ask(prompt):
    """Read input and make Ctrl+C/EOF exit cleanly."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        raise SystemExit


def show_menu():
    print("\n--- Banking Management System ---")
    print("1. Create account")
    print("2. Deposit money")
    print("3. Withdraw money")
    print("4. Check balance")
    print("5. View transaction history")
    print("6. View all accounts")
    print("7. Exit")


def money(value):
    return f"Rs. {value:,.2f}"


def create_account(service):
    account = service.create_account(
        ask("Enter 6-digit account number: "),
        ask("Enter account holder name: "),
        ask("Enter opening balance (or 0): ") or 0,
    )
    print(f"Account created successfully. Current balance: {money(account['balance'])}")


def deposit(service):
    balance = service.deposit(ask("Enter account number: "), ask("Enter deposit amount: "))
    print(f"Deposit successful. Current balance: {money(balance)}")


def withdraw(service):
    balance = service.withdraw(ask("Enter account number: "), ask("Enter withdrawal amount: "))
    print(f"Withdrawal successful. Current balance: {money(balance)}")


def check_balance(service):
    account = service.get_account(ask("Enter account number: "))
    print(f"Account holder: {account['name']}")
    print(f"Current balance: {money(account['balance'])}")


def history(service):
    account = service.get_account(ask("Enter account number: "))
    print(f"\nTransaction history for {account['name']}")
    if not account["transactions"]:
        print("No transactions recorded yet.")
        return
    print(f"{'Date':19}  {'Type':16} {'Amount':>12}  {'Balance after':>14}")
    print("-" * 68)
    for item in account["transactions"]:
        print(
            f"{item['date']:19}  {item['type']:16} "
            f"{money(item['amount']):>12}  {money(item['balance_after']):>14}"
        )


def all_accounts(service):
    accounts = service.list_accounts()
    if not accounts:
        print("No accounts have been created yet.")
        return
    print(f"\n{'Account No.':12} {'Name':25} {'Balance':>14}")
    print("-" * 55)
    for number, account in accounts:
        print(f"{number:12} {account['name']:25} {money(account['balance']):>14}")


def run():
    service = BankService(JSONStorage())
    print("Welcome to the Banking Management System")
    while True:
        show_menu()
        choice = ask("Choose an option (1-7): ")
        if choice == "7":
            print("Thank you for using the Banking Management System.")
            return
        try:
            if choice == "1":
                create_account(service)
            elif choice == "2":
                deposit(service)
            elif choice == "3":
                withdraw(service)
            elif choice == "4":
                check_balance(service)
            elif choice == "5":
                history(service)
            elif choice == "6":
                all_accounts(service)
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")
        except (BankError, StorageError) as error:
            print(f"Error: {error}")
