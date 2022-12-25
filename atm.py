"""This module contains program for customers to make transactions."""
from sql import *
from functions import *

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
                    continue
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
            print('Invalid entry.')
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
