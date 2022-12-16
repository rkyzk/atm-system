from sql import *
import hashlib

def validate_val(val):
    if val.isdigit():
        return True
    elif len(val) < 4:
        return False 
    elif val[-3] == "." and val[:-3].isdigit() and val[-2:].isdigit():
        return True
    else:
        return False

def collect_val(type_val):
    while True:
        dp = input(f"Enter {type_val} (): ")
        if not validate_val(dp):
            print("Invalid entry.")
            time.sleep(1.5)
        elif dp.isdigit():
            decimal_val = dp + ".00"
            return decimal_val
        else:
            return dp

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
            print("Please enter a valid.")
        else:
            return num

# In a real setting, the user will insert his/her card,
# and the machine will read off thire user_ID, 
# so there's no need to validate the IDs. 
# But for the sake of this program, I prepared validation
# since the user wll input it manually.

# check if the given user ID is an integer, since only int can be sent as an argument
# to function "get_user_info"
while True:
    user_id = input("Enter your user ID: ")
    if not user_id.isdigit():
        print("Invalid entry.  Please try again, "
            "or exit the program by pressing 'ctrl + c'")
        continue   
    # Get user info of the given ID from DB.  If no user exists with the ID,
    # ask the user to reenter their ID.
    user = get_user_info(int(user_id))
    if user == None:
        print("Invalid entry.  Please try again, "
            "or exit the program by pressing 'ctrl + c'")
        continue
    else:
        break

# if the card has been deactivated (if it has a flag value of "s" in Table Users.)
# tell the user to call personnel.
if user[8] == "s":
    print("Your card has been suspended.\nPlease call "
        "the number on the back of your card for assistance.")
    exit()
# Let the user input their pin.  If they get it wrong 4 times,
# the card will be deactivated (the flag of the user info in DB
# will be set to "s" for "suspend.")
n = 0  # index for the loop
while n < 4:
        unhashed = input('Enter your pin: ')
        if validate_pin(user_id, unhashed):
            print('\nLogin Success\n')
            break
        else:
            print("The pin is wrong.  Please try again.")
            n += 1
            continue
else:
    # After 4 wrong entries, block further login attempts by changing the flag to 's' in DB
    print("you're here")
    deactivate(user_id)
    exit()

"""
# Set values in User class object user and the current date into variables
name = user[0] + " " + user[1]
svg_acct_id = user[6]
check_acct_id = user[7]
date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

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
            amount = collect_val('Enter the amount you wish to withdraw: ')
            withdraw(amount, check_acct_id, user_id)
            break
        if choice == "b":
            # In real cases the user will insert money, and the machine will count the value,
            # but in this program, let the user enter the amount he/she deposits.
            amount = collect_val('Enter the amount of money you are depositing: ')
            print(amount)
            deposit(amount, check_acct_id, user_id)
            break
        if choice == "c":
            while True:
                option = input("\nDo you wish to make a transfer from your savings account,\n"
                               "or from your checking account?  Enter 'a' for savings account\n"
                               "'b' for checking account: ").lower()
                if option == 'a':
                    acct_id = svg_acct_id
                elif option == 'b':
                    acct_id = check_acct_id
                else:
                    print("Invalid entry.  Enter 'a' or 'b'.")
                    continue
                while True:
                    recip_acct_num = get_number("Enter the recipient's account number: ")
                    list_recip_info = get_recip_info(recip_acct_num)
                    if int(recip_acct_num) == acct_id:
                        print("You entered the ID of the account from which you wish to"
                              "make a transfer.  Please enter an account ID to which "
                              "you will transfer money.")
                        continue
                    elif list_recip_info == None:                # can I put 121 right before this line?
                        print(f"The given account ID {recip_acct_num} is not valid.")
                        while True:
                            option = input("Enter 'a' to abort the transaction, 'b' to continue: ").lower()
                            if option == "a":
                                exit()
                            elif option == "b":
                                break
                            else:
                                "Invalid entry."
                        continue
                    else:
                        amount = get_number("The amount to transfer: ")
                        trs_notes = input("Enter transactions notes(optional): ")
                        recip_id, recip = list_recip_info
                        print(f"You wish to transfer ${amount} to \n{recip} \n"
                              f"Account ID: {recip_acct_num}")
                    while True:
                        option = input("Enter 'y' to proceed with this transfer \n"
                                       "or enter 'n' to make changes: ").lower()
                        if option in ["y", "n"]:
                            break
                        else:
                            print("Invalid entry.")
                    if option == "y":
                        break
                    if option == "n":
                        continue
                boo = transfer(name, user_id, check_acct_id, int(amount), recip,
                         recip_id, recip_acct_num, trs_notes, date)
                if boo == False:
                    exit()
                else:
                    break
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
"""