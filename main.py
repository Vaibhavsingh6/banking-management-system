balance = 10000

while True:
    print("\n====== BANKING SYSTEM ======")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = input("Enter Your Choice: ")

    if choice == "1":
        print("Balance:", balance)

    elif choice == "2":
        amount = float(input("Enter Your Deposit Amount: "))

        if amount <= 0:
            print("Invalid Amount....")
        else:
            print("Amount Deposited...")
            print("Old Balance:", balance)

            balance = balance + amount

            print("Deposit Amount:", amount)
            print("New Balance:", balance)

    elif choice == "3":
        withdraw = float(input("Enter Your Withdraw Amount: "))

        if withdraw <= 0:
            print("Invalid Amount.....")

        elif withdraw > balance:
            print("Insufficient Balance....")

        else:
            print("Amount Withdrawal...")
            print("Old Balance:", balance)

            balance = balance - withdraw

            print("Withdrawal Amount:", withdraw)
            print("New Balance:", balance)

    elif choice == "4":
        print("Thank you for using the Banking System")
        break

    else:
        print("Invalid Choice.....")