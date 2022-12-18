from sql import *
import hashlib

def validate_transfer_val(val):
    """
    Return "True" if the argument "val" is a non-zero
    whole number or a positive number with two decimal digits.
    (e.g. '50' or '50.00')
    """
    if val in ["0", "0.00"]:
        return False
    if val.isdigit():
        return True
    elif len(val) < 4:
        return False
    elif val[-3] == "." and val[:-3].isdigit() and val[-2:].isdigit():
        return True
    else:
        return False

def collect_transfer_val(msg):
    """
    Print "msg" and have the users input a value and validate it
    by "validate_transfer_val()."  If "False" is returned,
    prompt them to reenter a valid value.
    Otherwise if the input "value" is an integer,
    add two decimal digits ".00" and return the value.  If "value"
    already has two decimal digits, return it as it is.
    """
    while True:
        value = input(msg)
        if not validate_transfer_val(value):
            print("Invalid entry. Enter values with or without "
                  "number of cents (e.g. '50' or '50.00').")
            continue
        elif value.isdigit():
            decimal_val = value + ".00"
            return decimal_val
        else:
            return value

def validate_val(val):
    #Return "True" if the argument is a multiple of 10.
    #Otherwise return "False."
    if val.isdigit and val not in ["", "0"] and val.endswith("0"):
        return True
    else:
        return False

def collect_val(msg):

    #If the argument "msg" doesn't pass validate_val function,
    #prompt the user to reenter a valid value.  Otherwise add
    #two decimal digits ".00" to the value and return it.
    
    while True:
        value = input(f"Enter {msg}: ")
        if not validate_val(value):
            print("Invalid entry.")
        elif value.isdigit():
            decimal_val = value + ".00"
            return decimal_val
        else:
            return value

def validate_pin(user_id, unhashed):
    """
    Get the salt and the stored key for the given user ID from the database,
    hash the argument "unhashed," and compare the new key with the stored key.
    Return "True" if they are identical, otherwise return "False."
    """
    user = get_user_info(user_id)
    salt = user[4]
    new_key = hashlib.pbkdf2_hmac('sha256', unhashed.encode('utf-8'),
                                  salt, 100000, dklen=128)
    if new_key == user[5]:
        return True
    else:
        return False

def get_number(msg):
    """
    Print "msg" and prompt the user to enter a value.
    Return the value if the input is a whole number.
    If not, prompt the user to reenter a value.
    """
    while True:
        num = input(msg)
        if num.isdigit():
            return num
        else:
            print("Please enter a valid ID.")
            continue                                 # needed?

def display_with_spaces(list):
    """
    Print items in the argument "list" with the numbers of spaces
    indicated in "list_num."
    """
    list_num = [25, 20, 30, 35, 10]
    str = ""
    for n, item in enumerate(list):
        space = " "
        num = list_num[n] - len(item)
        str += item + space*num
    print(str)

def print_row(list):
    """
    Using "display_with_spaces" function,
    print each row in the argument "list."
    """
    for item in list:
        display_with_spaces(item)

def validate_len(num):
    """
    Have the users input notes and check the length.
    If the length is equal to or less than 35 characters,
    return the input.  Otherwise prompt them to reenter notes.
    """
    while True:
        trs_notes = input(f"Enter transfer notes (optional, "
                          f"max {num} characters): ")
        if len(trs_notes) <= num:
            return trs_notes
        else:
            print(f"\nYou entered more than {num} characters.")
            continue

# In a real setting, the users will insert thier cards,
# and the machine will read off thier IDs,
# so there's no need to validate the user IDs.
# But in this program I prepared validation
# since the users will input their IDs manually.

while True:
    # Let the users enter their IDs and check if the input is a whole number.
    # This check is necessary since only int values can be sent to DB
    # to search the ID.
    user_id = get_number("Enter your user ID: ")
    # Get user info of the given ID from DB.
    # If no user with the ID is found, have the users reenter their IDs.
    user = get_user_info(int(user_id))                          # ok?
    if user is None:
        print("Invalid entry.")
        continue
    else:                   # cut?
        break
# If the card has been deactivated (if the flag value is set to "s" in table
# "Users," tell the users to call personnel, and terminate the program.
if user[8] == "s":
    print("\nYour card has been deactivatd.\nPlease call "
          "the number on the back of your card for assistance.")
    exit()
# Let the users input their pin.  If they get it wrong 4 times,
# the card will be deactivated (the flag value of the user in DB
# will be set to "s"
n = 0  # index of the loop
while n < 4:
    unhashed = input('Enter your pin: ')
    if validate_pin(user_id, unhashed):
        print('\nLogin Success\n')
        break
    if n < 3:
        print("The pin is wrong.  Please try again.")
        n += 1
        continue
    else:
        print("\nLogin failed 4 times.")
        # After 4 wrong entries, block further login attempts
        # by setting the flag to 's'
        deactivate(user_id)
        exit()
# Set user info that was stored in DB into variables.
name = " ".join([user[0], user[1]])
svg_acct_id = user[6]
check_acct_id = user[7]

print("*****************")
print(f"     Hello!")
print("*****************")
# Have the users select the transaction they want to make.
while True:
    print("\nSelect the type of transaction you wish to make:\n")
    print('a. Withdrawal')
    print('b. Deposit')
    print('c. Transfer')
    print('d. View your account balances')
    print('e. View your recent transactions (from the past 30 days')
    print('f. Exit\n')
    while True:
        choice = input('Enter a-f: ').lower()
        if choice == "a":         # Withdrawal
            amount = collect_val("Enter how much you'd like to withdraw "
                                 "in a multiple of 10: $")
            # Update the balance and transaction history of the user.
            withdraw(amount, check_acct_id, user_id)
            break
        if choice == "b":         # Deposit
            # In real setting the users will insert money, and the machine
            # will count the value, but in this program, let the users enter
            # the value.
            amount = collect_val('Enter the amount of money you are '
                                 'depositing in a multiple of 10: $')
            # Update the balance and transaction history of the user.
            deposit(amount, check_acct_id, user_id)
            break
        if choice == "c":         # Transfer
            while True:
                option = input("\nDo you wish to make a transfer "
                               "from your savings account,\n"
                               "or from your checking account?\n"
                               "Enter 'a' for savings account\n"
                               "'b' for checking account: ").lower()
                if option == 'a':
                    acct_id = svg_acct_id
                    acct_type = "savings"
                elif option == 'b':
                    acct_id = check_acct_id
                    acct_type = "checking"
                else:
                    print("\nInvalid entry.  Enter 'a' or 'b'.\n")
                    continue
                while True:
                    # Have the users enter the recipient's account ID.
                    recip_acct_id = get_number("\nEnter the recipient's "
                                               "account ID: ")
                    # Get the recipient's information from DB.
                    list_recip_info = get_recip_info(recip_acct_id)
                    # In case the account ID from which the users want
                    # to transfer the money is entered, tell them to reenter
                    # the right account ID of the recipient.
                    if int(recip_acct_id) == acct_id:
                        print("\nYou entered the ID of the account "
                              "from which you will make a transfer.\n"
                              "Please enter the account ID of "
                              "the recipient.")
                        continue
                    # If the given account ID is not found in DB,
                    # tell them to reenter a valid ID.
                    elif list_recip_info is None:
                        print(f"\nThe given account ID {recip_acct_id} "
                              f"is not valid.")
                        while True:
                            option = input("\nEnter 'a' to abort "
                                           "the transaction, "
                                           "'b' to continue: ").lower()
                            if option == "a":
                                print("Bye.  Have a nice day!")
                                exit()
                            elif option == "b":
                                break
                            else:
                                "\nInvalid entry."
                        continue
                    else:
                        # Collect transfer amount.
                        amount = collect_transfer_val("Enter the amount "
                                                      "you will transfer: ")
                        # Have the user enter transfer notes (max 35
                        # characters).  Check if the length is equal to
                        # or less than 35 characters.
                        trs_notes = validate_len(35)
                        recip_user_id, recip = list_recip_info
                        # Print the transfer detail for confirmation.
                        print(f"\nYou will transfer ${amount} to\n{recip}\n"
                              f"Account ID: {recip_acct_id}\n"
                              f"Transaction notes: {trs_notes}")
                    while True:
                        # Ask the users if the transfer can be carried out,
                        # or changes need to be made.
                        print(type(recip_acct_id))
                        option = input("\nEnter 'a' to proceed with "
                                       "this transfer,\n"
                                       "enter 'b' to make changes: ").lower()
                        if option in ["a", "b"]:
                            break
                        else:
                            print("\nInvalid entry.")
                            continue
                    if option == "a":
                        break
                    if option == "b":
                        continue
                # Make updates regarding this transfer in the DB
                transfer(name, user_id, acct_id, acct_type, amount,
                         recip, recip_user_id, trs_notes, recip_acct_id)
                break
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
            # Store the balance of the savings account
            # and that of the checking account.
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
            continue
    while True:
        # Ask if the users want to make further transactions.
        # If they do, send them back to the selections of transactions.
        # If not, terminate the program.
        choice = input("Would you like to make further transactions? "
                       "(y/n): ").lower()
        if choice == "n":
            print("Thank you.  Have a nice day!")
            exit()
        elif choice == "y":
            break
        else:
            print("Invalid entry.  Please enter 'y' or 'n'")
            continue