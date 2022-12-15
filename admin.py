from sql import * 
import decimal
D=decimal.Decimal
import random
from datetime import datetime
import hashlib
import os
import time
from User import User

def get_pin():
    """
    Generate a random 6-digit pin and return it.
    return str_pin -- pin
    """
    str_pin = ""  
    for n in range(6):
        str_pin += str(random.randrange(10))
    return str_pin

def hash_pin_with_salt(pin, salt):
    """
    Hash the pin with a given salt and return the key.
    """
    key = hashlib.pbkdf2_hmac(
        'sha256',
        pin.encode('utf-8'),  # convert the pin to bytes
        salt,
        100000,  # number of iterations of SHA256
        dklen=128  # get a 128-byte key
    )
    return key

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

def validate_name(name):
    """
    Check if the name string contains only alphabets.
    If so, return True, if not return False.

    Argument:
    name -- name to validate
    """
    letters = name.replace(" ", "")
    if letters.isalpha():
        return True
    else:
        return False

def collect_name(fill_in_the_b):
    """
    Prompt the user to enter first or last name.
    Have the input validate.  If it passes the validation,
    return the input. If not prompt the user to reenter the name. 

    Argument:
    f_l_name -- specifies first or last name
    """
    while True:
        name = input(f"Enter the customer's {fill_in_the_b}: ")
        if validate_name(name):
            return name
        else:
            print("Invalid entry (enter only alphabets).")
            time.sleep(1.5)

def get_ids(code):
    """
    Get a user ID, savings account ID and checking account ID for a new customer 
    based on their selection of the bank.

    Argument:
    code -- the bank selection (a: North Bank; b: East Bankl c: South Bank)
    Return value:
    acct_info  -- list containing the bank name, user ID and account IDs
    """
    while True:
        # Assign the bank name to the variable 'bank'.
        if code == "a":
            bank = "North Bank"
            break
        if code == "b":
            bank = "East Bank"
            break
        if code == "c":
            bank = "South Bank"
            break
        else:  # correct------------------------------?
            print("Invalid entry.  Please try again.")
            time.sleep(1.5)

    user_id = get_user_id(code)
    new_accts = get_acct_ids(code)
    acct_info = []
    # Store the bank name, user ID and account IDs in the list "account_info," and return the list
    acct_info.append(bank)
    acct_info.append(user_id)
    acct_info.append(new_accts)
    return acct_info

def print_data(user):
    """
    Print the information of a user.

    Argument:
    user -- User class object
    """
    print(f"Name: {user.fname} {user.lname}")
    print(f"User ID: {user.user_id}")
    print(f"Bank Name: {user.bank}")
    print(f"Savings Account ID: {user.svg_acct_id}")
    print(f"Checking Account ID: {user.check_acct_id}")
    print(f"--Initial Deposits--")
    print(f"Savings Account: ${user.svg_dp}")
    print(f"Checking Account: ${user.check_dp} \n")

print("****************************")
print("          Hello!")
print("****************************\n")
print("This terminal is for creating new accounts.\n")
time.sleep(2)
# Collect the customer's first name and validate it
fname = collect_name("first name")
# Collect the customer's first name and validate it
lname = collect_name("last name")
# the customer's full name       
holder = fname + " " + lname
# Have the user select a bank
print("\nAt which bank are you creating accounts?")
while True:
    print("Enter 'a' for North Bank\n'b' for East Bank\n'c' for South Bank.")
    code = input("Your input: ").lower()  # The bank code
    if code not in ["a", "b", "c"]:
        print("Invalid entry.")
        time.sleep(1.5)
    else:
        break
svg_dp = collect_val("Initial deposit in savings account")
check_dp = collect_val("Initial deposit in checking account")
# Get user ID, account IDs and the bank name and store them in the following variables
bank, user_id, new_accts = get_ids(code)
svg_acct_id, check_acct_id = new_accts
# Get a pin & salt, and then hash the pin to get a key
salt = os.urandom(32)
pin = get_pin()
key = hash_pin_with_salt(pin, salt)
# In real situations the pin will be shown only to the customer
# but here, it will be printed so the program can be tested.
print(f"Pin: {pin}")
print(key) # remove this later
print(salt)  # remove this later
print(user_id)
print(svg_acct_id, check_acct_id, bank)

date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Store all user info into User class object "user" 
user = User(fname, lname, holder, bank, user_id, salt, key, svg_acct_id, 
            check_acct_id, svg_dp, check_dp, date)
while True:
    # Print the user information for confirmation before inserting it to DB
    print("\n----------------------------------")
    print("Confirm the following information")
    print("----------------------------------")
    print_data(user)
    # Ask if the data can be stored as it was printed or needs to be changed.
    print("Would you like to \na: insert the above data into DB\n"
          "b: make changes\nc: terminate the session\n")
    confirm = input("Enter 'a', 'b' or 'c': ").lower()
    if confirm not in ['a', 'b', 'c']:
        print("\nInvalid entry.  Please try again.")
        time.sleep(1.5)
        continue
    if confirm == "a":
        print("\nThe data will be stored into DB...")
        break
    if confirm == "c":
        print("\nAre you sure you want to terminate the session?\n"
              "All information will be lost.\n")
        while True:
            print("Enter 'a' to terminate, 'b' to go back to the previous options.")
            option = input("Your input: ").lower()
            if option == "a":
                print("Bye!  Have a nice day.")
                exit()
            if option == "b":
                break
            else:
                print("\nInvalid entry.")
                continue
    else:                                                        # ----------ok?
        # Let the administrator choose which item to update.
        while True:
            print("Select the item you wish to change.\n")
            print("a: First name")
            print("b: Last name")
            print("c: Bank")
            print("d: Deposit in savings account")
            print("e: Deposit in checking account")
            print("f: Go back to the previous options\n")
            choice = input("Enter a-f: ").lower()
            # Let the administrator make changes in the customer's information
            if choice not in ['a', 'b', 'c', 'd', 'e', 'f']:
                print("Invalid entry. Please try again.\n")
                continue
            elif choice == 'a':
                user.fname = collect_name("correct first name")
                break
            elif choice == 'b':
                user.lname = collect_name("correct last name: ")
                break
            elif choice == 'c':
                # Change the bank, thereby get a new user ID and account IDs.
                while True:
                    print("Enter \n'a' for North Bank \n'b' for East Bank\n'c' for South Bank.")
                    code = input("Your input: ").lower()  # The bank code
                    if code not in ['a', 'b', 'c']:
                        print("Invalid entry.\n")
                        continue
                    else:
                        user.bank, user.user_id, new_accts = get_ids(code)
                        user.svg_acct_id, user.check_acct_id = new_accts
                        print(user.user_id)
                        break
                break    
            elif choice == 'd':
                user.svg_dp = collect_val("Initial deposit in savings account: ")
                break
            elif choice == 'e':
                user.check_dp = collect_val("Initial deposit in checking account: ")
                break               
            else:
                break
# call the function that inserts data into DB
create_new_accounts(user)
            


#insert sample users
date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

salt = os.urandom(32)
pin = "111111"
key = hash_pin_with_salt(pin, salt)

# user = User("John", "Smith", "John Smith", "North Bank", 100001, salt, key, 1100001, 1200001, '1000.00', '1000.00', date)
# user = User("Katie", "Baker", "Katie Baker", "East Bank", 200001, salt, key, 2100001, 2200001, '1000.00', '1000.00', date)
user = User("Jacky", "Adams", "Jacky Adams", "South Bank", 300001, salt, key, 3100001, 3200001, '1000.00', '1000.00', date)

# create_new_accounts(user)