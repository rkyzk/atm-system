print("*************************")
print(f"     Hello\n")

print("Select the type of transaction you wish to undertake:")
print('a. Withdrawal')
print('b. Deposit')
print('c. Transfer')
print('d. View your balance')
print('e. View recent transactions')
print('f. Exit')

choice = input('Enter a-f: ').lower()
    if choice == "a":
        amount = input('Enter the amount you wish to withdraw: ')
        withdraw()
    elif choice == "b":
        # In real settings the user will insert money, and the machine will
        # count the inserted money, but here, let the user enter the deposit amount.
        amount = input('Enter the amount of money you are depositing: ')
        deposit(amount, acct_id)
    elif choice == "c":
        recip_acct_id = input("Enter the recipient's account number: ")
        amount = input("The amount to transfer: ")
        trs_notes = input("Enter transactions notes(optional): ")
        transfer(user_id, amount, recip_acct_id, trs_notes)
    elif choice == "d":
        list = display_balance(user_id)
    elif choice == "e":
        list = display_transactions(user_id)
    elif choice == "f":
        exit()
    else:
        print("Invalid entry")