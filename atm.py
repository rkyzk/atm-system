from sql import *
import hashlib

def validate_transfer_val(val):
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
    while True:
        value = input(msg)
        if not validate_transfer_val(value):
            print("Invalid entry. Enter values with or without number of cents (e.g. '50' or '50.00').")
            continue
        elif value.isdigit():
            decimal_val = value + ".00"
            return decimal_val
        else:
            return value

def validate_val(val):
    if val.isdigit and val not in ["", "0"] and val[-1] == "0":
        return True
    else:
        return False

def collect_val(msg):
    while True:
        value = input(msg)
        if not validate_val(value):
            print("Invalid entry.")
            continue
        else:
            decimal_val = value + ".00"
            return decimal_val
        
def validate_pin(user_id, unhashed):
    user = get_user_info(user_id)
    salt = user[4]
    new_key = hashlib.pbkdf2_hmac('sha256', unhashed.encode('utf-8'), salt, 100000, dklen=128)
    if new_key == user[5]:
        return True
    else:
        return False

def get_number(msg):
    """
    Validate if the input is a number.  If so, return the number.
    If not, prompt the user to reenter a number.
    """
    while True:
        num = input(msg)
        if not num.isdigit():
            print("Please enter a valid ID.")
        else:
            return num

def print_row(list):
    for item in list:
        display_with_spaces(item)

def display_with_spaces(list):
    list_num = [32, 22, 32, 20, 10]
    str = ""
    for n, item in enumerate(list):
        space = " "
        num = list_num[n] - len(item)
        str += item + space * num
    print(str)

# In a real setting, the users will insert thier cards,
# and the machine will read off thier IDs, 
# so there's no need to validate the values. 
# But for the sake of this program, I prepared validation
# since the users will input their IDs manually.

# check if the given value consists of numbers only, 
# since non numeric values cause errors when they are set as arguments
# for "get_user_info" function.
while True:
    user_id = input("Enter your user ID: ")
    if not user_id.isdigit():
        print("Invalid entry.  Please try again.")
        continue   
    # Get user info of the given ID from DB.  If no user with the ID exists,
    # ask the users to reenter their IDs.
    user = get_user_info(int(user_id))     #  is this ok?
    if user == None:
        print("Invalid entry.  .")
        continue
    else:      # cut?
        break

# If the card has been deactivated (if the flag value is set to "s" in Table Users)
# tell the user to call personnel.
if user[8] == "s":
    print("\nYour card has been deactivatd.\nPlease call "
        "the number on the back of your card for assistance.")
    exit()
# Let the user input their pin.  If they get it wrong 4 times,
# the card will be deactivated (the flag of the user info in DB
# will be set to "s" ("s "for "suspended.")
n = 0  # index for the loop
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
        # After 4 wrong entries, block further login attempts by changing the flag to 's' in DB
        deactivate(user_id)
        exit()

# Set values that were stored in User class object "user" into variables.
name = user[0] + " " + user[1]
svg_acct_id = user[6]
check_acct_id = user[7]

print("*****************")
print(f"     Hello!")
print("*****************")
while True:
    print("\nSelect the type of transaction you wish to undertake:\n")
    print('a. Withdrawal')
    print('b. Deposit')
    print('c. Transfer')
    print('d. View your account balances')
    print('e. View recent transactions (from the past 30 days')
    print('f. Exit\n')
    while True:
        choice = input('Enter a-f: ').lower()
        if choice == "a":
            amount = collect_val("Enter how much you'd like to withdraw in multiples of 10: $")
            withdraw(amount, check_acct_id, user_id)
            break
        if choice == "b":
            # In real cases the user will insert money, and the machine will count the value,
            # but in this program, let the user enter the amount he/she deposits.
            amount = collect_val('Enter the amount of money you are depositing in multiples of 10: $')
            deposit(amount, check_acct_id, user_id)
            break
        if choice == "c":
            while True:
                option = input("\nDo you wish to make a transfer from your savings account,\n"
                               "or from your checking account?\nEnter 'a' for savings account\n"
                               "'b' for checking account: ").lower()
                if option == 'a':
                    acct_id = svg_acct_id
                elif option == 'b':
                    acct_id = check_acct_id
                else:
                    print("\nInvalid entry.  Enter 'a' or 'b'.")
                    continue
                while True:
                    recip_acct_num = get_number("\nEnter the recipient's account ID: ")
                    list_recip_info = get_recip_info(recip_acct_num)
                    if int(recip_acct_num) == acct_id:
                        print("\nYou entered the ID of the account from which you will "
                              "make a transfer.\nPlease enter the account ID of "
                              "the recipient.")
                        continue
                    elif list_recip_info == None:
                        print(f"\nThe given account ID {recip_acct_num} is not valid.")
                        while True:
                            option = input("\nEnter 'a' to abort the transaction, "
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
                        amount = collect_transfer_val("Enter the amount you will transfer: ")
                        trs_notes = input("\nEnter transactions notes(optional): ")
                        recip_id, recip = list_recip_info
                        print(f"\nYou will transfer ${amount} to \n{recip}\n"
                              f"Account ID: {recip_acct_num}\nTransaction notes: {trs_notes}")
                    while True:
                        option = input("\nEnter 'a' to proceed with this transfer,\n"
                            "enter 'b' to make changes: ").lower()
                        if option in ["a", "b"]:
                            break
                        else:
                            print("\nInvalid entry.")
                    if option == "a":
                        break
                    if option == "b":
                        continue
                transfer(name, user_id, acct_id, amount, recip,
                    recip_id, trs_notes, recip_acct_num)
                break
            break
        if choice == "d":
            list = display_balance(user_id)
            print(f"\nYour savings account ID: {list[0][0]}")
            print(f"Balance: ${list[0][1]}")
            print(f"\nYour checking account ID: {list[1][0]}")
            print(f"Balance: ${list[1][1]}\n")
            break
        if choice == "e":
            list = display_transactions(user_id)
            svg_list = []
            check_list = []
            for item in list:
                if str(item[0])[1] == "1":
                    list = []
                    for n in range(1, 6):
                        list.append(item[n])
                    svg_list.append(list)
                else:
                    list = []
                    for n in range(1, 6):
                        list.append(item[n])
                    check_list.append(list)

            headings = ["Date", "Transaction type", "Transfer to/from", "Transfer notes",
                        "Amount"]
            print("========================================================================")
            print("***Savings account transactions\n")
            display_with_spaces(headings)
            print_row(svg_list)
            print("========================================================================")
            print("***Checking account transactions\n")
            display_with_spaces(headings)
            print_row(check_list)
            break
        if choice == "f":
            print("Bye.  Have a nice day!")
            exit()
        else:
            print('Invalid entry.  Please try again.')  
    while True:
        choice = input("Would you like to make further transactions? (y/n): ").lower()
        if choice == "n":
            print("Thank you.  Have a nice day!")
            exit()
        elif choice == "y":
            break
        else:
            print("Invalid entry.  Please enter 'y' or 'n'")