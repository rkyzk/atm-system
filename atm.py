from sql import *


user_id = 1000001
acct_id = 2000001




print("*****************")
print(f"     Hello!")
print("*****************")
while True:
    print("\nSelect the type of transaction you wish to undertake:\n")
    print('a. Withdrawal')
    print('b. Deposit')
    print('c. Transfer')
    print('d. View your balance')
    print('e. View recent transactions')
    print('f. Exit\n')
    while True:
        choice = input('Enter a-f: ').lower()
        if choice == "a":
            amount = input('Enter the amount you wish to withdraw: ')
            withdraw(user_id, amount)
            print("Please take the money and your card.")
            break
        if choice == "b":
            # In real settings the user will insert money, and the machine will
            # count the inserted money, but here, let the user enter the deposit value.
            amount = input('Enter the amount of money you are depositing: ')
            deposit(amount, acct_id)
            print(f"${amount} was depositted to your account.")
            break
        if choice == "c":
            recip_acct_id = input("Enter the recipient's account number: ")
            amount = input("The amount to transfer: ")
            trs_notes = input("Enter transactions notes(optional): ")
            transfer(user_id, amount, recip_acct_id, trs_notes)
            print(f"${amount} was transferred to {recip_acct_id}.")
            break
        if choice == "d":
            list = display_balance(user_id)
            print(list)
            break
        if choice == "e":
            list = display_transactions(user_id)
            print(list)
            break
        if choice == "f":
            print("Have a nice day!")
            exit()
        else:
            print("Invalid entry.")
    while True:
        choice = input("Do you wish to make further transactions? (y/n): ")
        if choice == "n":
            print("Thank you.  Have a nice day!")
            exit()
        elif choice == "y":
            break
        else:
            print("Invalid entry.")