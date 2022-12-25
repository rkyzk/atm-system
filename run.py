from user_partial_info import UserPartialInfo
from functions import *
import os
import time

print("Choose the program you want to run.\n"
      "a. terminal for creating new accounts for customers "
      "(for bank personnel)\n"
      "b. ATM terminal (for customers)")
while True:
    choice = input("Enter 'a' or 'b': \n")
    if choice in ['a', 'b']:
        break
    else:
        print("Invalid entry")
# Program for bank personnel till line 146.        
if choice == "a":
    # Have the user login with a username and a password.
    # Validate the two inputs. If login fails 3 times,
    # the program will be terminated.
    n = 0
    while n < 3:
        username = input("Username: \n")
        password = input("Password: \n")
        if validate_admin_pass(username, password):
            print("Login success")
            break
        else:
            if n < 2:
                print("The given username or the password is wrong. "
                    "Please try again.")
                n += 1
            else:
                print("Login failed three times. The program will be "
                      "terminated.\nPlease reach out to authorized personnel.")
                exit()

    print("****************************")
    print("         Hello!")
    print("****************************\n")
    print("This terminal is for creating new accounts.\n")
    time.sleep(1.5)
    # Collect the customer's first name and validate it.
    fname = collect_name("Enter the customer's first name: \n")
    # Collect the customer's first name and validate it.
    lname = collect_name("Enter the customer's last name: \n")
    # The customer's full name.
    holder = " ".join([fname, lname])
    # Have the user select a bank.
    print("\nAt which bank are you creating accounts?")
    # Get the bank code
    bank_code = collect_bank_code()
    # Input initial deposit values for each account.
    svg_dp = collect_mult_of_10("Enter initial deposit in savings account "
    "in a multiple of 10: \n")
	check_dp = collect_mult_of_10("Enter initial deposit in checking account "
    "in a multiple of 10: \n")
    # Get a pin & salt, and then hash the pin to get a key.
    pin = get_pin()
    salt = os.urandom(32)
    key = hash_pin_with_salt(pin, salt)
    # In real situations the pin will be shown only to the customer,
    # but here, it will be printed so checkers can test the program.
    print(f"Pin: {pin}\n")
    while True:
        # Print the user information for confirmation before inserting it into DB.
        print("----------------------------------")
        print("Confirm the following information")
        print("----------------------------------")
        print_data(fname, lname, bank_code, svg_dp, check_dp)
        # Ask if the data can be stored as printed above or need to be changed.
        print("Would you like to \na: insert the above data into DB\n"
              "b: make changes, or\nc: terminate the session\n")
        answer = input("Enter 'a', 'b' or 'c': \n").lower()
        if answer not in ['a', 'b', 'c']:
            print("\nInvalid entry. Please try again.")
            continue
        elif answer == "a":
            print("\nThe data will be stored into DB...")
            break
        elif answer == "c":
            print("\nAre you sure you want to terminate the session?")
            print("All information will be lost.\n")
            while True:
                print("Enter 'a' to terminate, "
                      "'b' to go back to the previous options.")
                option = input("Your input: \n").lower()
                if option == "a":
                    print("\nBye. Have a nice day!")
                    exit()
                elif option == "b":
                    break
                else:
                    print("\nInvalid entry.")
        else:
            # Let the user choose which item to correct.
            while True:
                print("Select the item you need to correct.\n")
                print("a: First name")
                print("b: Last name")
                print("c: Bank")
                print("d: Deposit value in savings account")
                print("e: Deposit value in checking account")
                print("f: Go back to the previous options\n")
                choice = input("Enter a-f: \n").lower()
                # Let the user make changes in the customer's information.
                if choice == 'a':
                    fname = collect_name("Enter the customer's "
                                         "correct first name: \n")
                    break
                if choice == 'b':
                    lname = collect_name("Enter the customer's "
                                         "correct last name: \n")
                    break
                if choice == 'c':
                    bank_code = collect_bank_code()
                    break
                if choice == 'd':
                    svg_dp = collect_mult_of_10("Enter initial deposit in "
                                                "savings account in "
                                                "a multiple of 10: \n")
                    break
                if choice == 'e':
                    check_dp = collect_mult_of_10("Enter initial deposit in "
                                                  "checking account in "
                                                  "a multiple of 10: \n")
                    break
                if choice == 'f':
                    break
                else:
                    print("\nInvalid entry. Please try again.")
    bank = get_bank(bank_code)
    # Store all user info in a User class object named "user."
    user_partial_info = UserPartialInfo(fname, lname, bank, salt, key,
    svg_dp, check_dp)
    # Insert the data into DB.
    user_id = create_new_accounts(user_partial_info)
    # Print IDs and balances of accounts
    list_balances = get_balances(user_id)
    print("The data below have been stored in the database:\n")
    print(f"Name: {fname} {lname}")
    print(f"User ID: {user_id}")
    print(f"Savings Account ID: {list_balances[0][0]}")
    print(f"Balance: ${list_balances[0][1]}")
    print(f"Checking account ID: {list_balances[1][0]}")
    print(f"Balance: ${list_balances[1][1]}\n")
# Program for customers (ATM terminal)    
else:
    # In real setting, the users will insert their cards, and the machine will
    # read off their IDs, so there's no need to validate the values.
    # But in this program I prepared validation since the users will input
    # their IDs manually.
    print("*****************")
    print("     Hello!")
    print("*****************")
    while True:
        # Let the users enter their IDs and check if the input is
        # a 7-digit whole number starting with bank code 1, 2 or 3.
        user_id = check_id("Enter your user ID: \n", 7)
        # Get user info of the given ID from DB.
        # If no user with the ID is found, have the users reenter their IDs.
        user = get_user_info(int(user_id))
        if user:
            break
        else:
            print("Invalid entry.")
    # If the card has been deactivated (if the flag value is set to "s" in table
    # "Users," tell the users to call personnel, and terminate the program.
    if user.flag == "s":
        print("\nYour card has been deactivatd.\nPlease call "
              "the number on the back of your card for assistance.")
        exit()
    # Let the users input their pin.  If they get it wrong 4 times,
    # the card will be deactivated (the flag value of the user will be set to
    # "s" -- "s" for "suspended")
    n = 0
    while n < 4:
        unhashed = input('Enter your pin: \n')
        if validate_pin(user_id, unhashed):
            print('\nLogin Success\n')
            break
        if n < 3:
            print("The pin is wrong.  Please try again.")
           n += 1
        else:
            n += 1
    else:
        print("\nLogin failed 4 times.")
        # Block further login attempts by setting the flag to "s."
        deactivate(user_id)
        exit()
    # Set the user's full name into variable "name."
    name = " ".join([user.fname, user.lname])
    # Have the users select the transaction they want to make.
    while True:
        print(f"Hello {name},\nSelect the type of transaction "
              "you wish to make:\n")
        print('a. Withdrawal')
        print('b. Deposit')
        print('c. Transfer')
        print('d. View your account balances')
        print('e. View your recent transactions (from the past 30 days')
        print('f. Exit\n')
        while True:
            choice = input('Enter a-f: \n').lower()
            if choice == "a":         # Withdrawal
                amount = collect_mult_of_10("Enter how much you'd like "
                                            "to withdraw in a multiple of 10: $\n")
                # Update the balance and transaction history of the user.
                withdraw(amount, user)
                break
            if choice == "b":         # Deposit
                # In real setting the users will insert money, and the machine
                # will count the value, but in this program, let the users enter
                # the value they are depositing.
                amount = collect_mult_of_10('Enter the amount of money you are '
                                            'depositing in a multiple of 10: $\n')
                # Update the balance and transaction history of the user.
                deposit(amount, user)
                break
            if choice == "c":         # Transfer
                while True:
                    option = input("\nDo you wish to make a transfer "
                                   "from your savings account,\n"
                                   "or from your checking account?\n"
                                   "Enter 'a' for savings account\n"
                                   "'b' for checking account: \n").lower()
                    if option == 'a':
                        acct_id = user.svg_acct_id
                        break
                    elif option == 'b':
                        acct_id = user.check_acct_id
                        break
                    else:
                        print("\nInvalid entry.  Enter 'a' or 'b'.")
                while True:
                    # Have the users enter the recipient's account ID
                    # and check the validity of the input.
                    recip_acct_id = check_id("\nEnter the recipient's "
                                             "account ID: \n", 8)
                    # Get the recipient's name from DB.
                    recipient = get_recipient(recip_acct_id)
                    # If the account ID is not found in DB, print the notes below.
                    if recipient is None:
                        print(f"\nThe given account ID {recip_acct_id} "
                              "is not valid.")
                        while True:
                            option = input("Enter 'a' to abort the transaction, "
                                           "'b' to continue: \n").lower()
                            if option == "a":
                                print("Bye.  Have a nice day!")
                                exit()
                            elif option == "b":
                                break
                            else:
                                print("\nInvalid entry.")
                        continue
                    # In case the account ID from which the users want
                    # to transfer the money is entered, tell them to reenter
                    # the right account ID of the recipient.
                    elif int(recip_acct_id) == acct_id:
                        print("\nYou entered the ID of the account from which "
                              "you will make a transfer.\nPlease enter "
                              "the account ID of the recipient.")
                    # Collect transfer amount.
                    amount = collect_val("Enter the amount "
                                         "you will transfer: \n")
                    # If there isn't enough money in the account,
                    # print the note below and terminate the program.
                    if not check_balance(acct_id, amount):
                        print("You don't have sufficient money in your "
                              "account to make this transfer.\n"
                              "The program will be terminated.")
                        exit()
                    # Have the users enter transfer notes (max 35
                    # characters).  Let them reenter the text if
                    # the length exceeds 35 characters.
                    trs_notes = validate_len(35)
                    # Print the transfer detail for confirmation.
                    print(f"\nYou will transfer ${amount} to\n{recipient}\n"
                          f"Account ID: {recip_acct_id}\n"
                          f"Transaction notes: {trs_notes}")
                    while True:
                        # Ask the users if the transfer can be carried out,
                        # or they want to make changes.
                        option = input("\nEnter 'a' to proceed with this "
                                       "transfer,\nenter 'b' to make "
                                       "changes: \n").lower()
                        if option in ["a", "b"]:
                            break
                        else:
                            print("Invalid entry")
                    if option == "a":
                        break
                # Make updates regarding this transfer in the DB
                transfer(user, acct_id, amount, recipient, recip_acct_id,
                         trs_notes)
                break
            if choice == "d":         # "View your balances" option
                # Get balances from DB and print them.
                list_balances = get_balances(user_id)
                print(f"\nYour savings account ID: {list_balances[0][0]}")
                print(f"Balance: ${list_balances[0][1]}")
                print(f"\nYour checking account ID: {list_balances[1][0]}")
                print(f"Balance: ${list_balances[1][1]}\n")
                break
            if choice == "e":        # "View your recent transactions" option
                # Get transaction records of the user.
                list_trans = get_transactions(user_id)
                # Sort the records into transactions around the savings account
                # and those around the checking account.
                svg_list = []
                check_list = []
                for item in list_trans:
                    # item[1] tells the account type: savings/checking.
                    if item[1] == "savings":
                        list = []
                        # "range(2, 7)" refers to date, trs_type, trs_to_or_from,
                        #  trs_notes, amount from "get_transactions" function
                        for n in range(2, 7):
                            list.append(item[n])
                        svg_list.append(list)
                    else:
                        # Collect records of the checking account.
                        list = []
                        for n in range(2, 7):
                            list.append(item[n])
                        check_list.append(list)
                # Get current balances.
                list_balances = get_balances(user_id)
                # Store the balances of both accounts in variables.
                svg_balance, check_balance = [list_balances[0][1],
                                              list_balances[1][1]]
                # Make a list of headings in the table of
                # transaction history.
                headings = ["Date", "Transaction", "Transfer to/from",
                            "Transfer notes", "Amount"]
                space = " "
                # Print the table
                print("====================================================")
                print("*Savings account transactions\n")
                display_with_spaces(headings)
                print_row(svg_list)
                print(f"\n{space*78}**Current balance:{space*14}${svg_balance}")
                print("====================================================")
                print("*Checking account transactions\n")
                display_with_spaces(headings)
                print_row(check_list)
                print(f"\n{space*78}**Current balance:"
                      f"{space*14}${check_balance}\n")
                break
            if choice == "f":  # Exit
                print("Bye.  Have a nice day!")
                exit()
            else:
                print('Invalid entry.  Please try again.')
        while True:
            # Ask if the users want to make further transactions.
            # If they do, send them back to the selections of transactions.
            # If not, terminate the program.
            choice = input("Would you like to make further transactions? "
                           "(y/n): \n").lower()
            if choice == "n":
                print("Thank you.  Have a nice day!")
                exit()
            elif choice == "y":
                break
            else:
                print("Invalid entry.  Please enter 'y' or 'n'")
