from sql import *
import random
from datetime import datetime
import hashlib
import os
import time
from User import User

def get_pin():
    """Generate a random 6-digit pin and return it."""
    str_pin = ""
    for n in range(6):
        str_pin += str(random.randrange(10))
    return str_pin

def hash_pin_with_salt(pin, salt):
    """Hash the pin with a given salt and return the key."""
    key = hashlib.pbkdf2_hmac(
        'sha256',
        pin.encode('utf-8'),  # convert the pin to bytes
        salt,
        100000,  # number of iterations of SHA256
        dklen=128  # get a 128-byte key
        )
    return key

def validate_val(val):
    """
    Return "True" if the argument is a multiple of 10.
    Otherwise return "False."
    """
    if val.isdigit and val not in ["", "0"] and val.endswith("0"):
        return True
    else:
        return False

def collect_val(msg):
    """
    Prompt the user to enter a value that "msg" specifies
    and validate it.  If "validate_val" function returns False,
    have the user reenter a valid value.   If True is returned,
    add two decimal digits ".00" to the value and return it.
    """
    while True:
        value = input(f"Enter {msg}: ")
        if not validate_val(value):
            print("Invalid entry.")
            continue
        elif value.isdigit():
            decimal_val = value + ".00"
            return decimal_val
        else:
            return value

def validate_name(name):
    """
    Return True if the name string contains only alphabets.
    Otherwise return False.
    """
    letters = name.replace(" ", "")
    if letters.isalpha():
        return True
    else:
        return False

def collect_name(f_lname):
    """
    Prompt the user to enter their first or last name.
    If the input passes the validation by validate_name function,
    return the input. If not, prompt the user to reenter their name.
    """
    while True:
        name = input(f"Enter the customer's {f_lname}: ")
        if validate_name(name):
            return name
        else:
            print("Invalid entry (enter only alphabets).")
            continue

def collect_bank_code():
    """
    Have the user select the bank and return the code.
    :return: code -- bank code                    #??
    """
    while True:
        print("Enter 'a' for North Bank\n'b' for East Bank\n"
              "'c' for South Bank.")
        code = input("Your input: ").lower()        # The bank code
        if code not in ["a", "b", "c"]:
            print("\nInvalid entry.")
            continue
    return code

def get_ids(code):
    """
    Get the bank name, a user ID, savings account ID
    and checking account ID for a new customer based on the bank code.
    """
    # Assign the bank name to variable 'bank'.
    if code == "a":
        bank = "North Bank"
    if code == "b":
        bank = "East Bank"
    if code == "c":
        bank = "South Bank"
    # Search the database and get the next available user ID.
    user_id = get_user_id(code)
    # Get the next available savings and checking account IDs.
    new_accts = get_acct_ids(code)
    acct_info = []
    # Store the bank name and IDs in the list
    # "account_info," and return the list
    acct_info.append(bank)
    acct_info.append(user_id)
    acct_info.append(new_accts)
    return acct_info

def print_data(user):
    """
    Print the information of the given user.
    """
    print(f"Name: {user.fname} {user.lname}")
    print(f"User ID: {user.user_id}")
    print(f"Bank Name: {user.bank}")
    print(f"Savings Account ID: {user.svg_acct_id}")
    print(f"Checking Account ID: {user.check_acct_id}")
    print(f"--Initial Deposits--")
    print(f"Savings Account: ${user.svg_dp}")
    print(f"Checking Account: ${user.check_dp}\n")

print("****************************")
print("          Hello!")
print("****************************\n")
print("This terminal is for creating new accounts.\n")
time.sleep(1.5)
# Collect the customer's first name and validate it.
fname = collect_name("first name")
# Collect the customer's first name and validate it.
lname = collect_name("last name")
# The customer's full name.
holder = fname + " " + lname
# Have the user select a bank.
print("\nAt which bank are you creating accounts?")
# Get
code = collect_bank_code()
# Get user ID, account IDs and the bank name and store them
# in the following variables.
bank, user_id, new_accts = get_ids(code)
svg_acct_id, check_acct_id = new_accts
# Input initial deposit values for each account.
svg_dp = collect_val("initial deposit in savings account")
check_dp = collect_val("initial deposit in checking account")
# Get a pin & salt, and then hash the pin to get a key.
pin = get_pin()
salt = os.urandom(32)
key = hash_pin_with_salt(pin, salt)
# In real situations the pin will be shown only to the customer,
# but here, it will be printed so checkers can test the program.
print(f"Pin: {pin}\n")
# Get the current date time.
date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Store all user info in a User class object named "user."
user = User(fname, lname, holder, bank, user_id, salt, key, svg_acct_id,
            check_acct_id, svg_dp, check_dp, date)
while True:
    # Print the user information for confirmation before inserting it into DB.
    print("----------------------------------")
    print("Confirm the following information")
    print("----------------------------------")
    print_data(user)
    # Ask if the data can be stored as printed above or need to be changed.
    print("Would you like to \na: insert the above data into DB\n"
          "b: make changes, or\nc: terminate the session\n")
    answer = input("Enter 'a', 'b' or 'c': ").lower()
    if answer not in ['a', 'b', 'c']:
        print("\nInvalid entry.  Please try again.")
        continue
    if answer == "a":
        print("\nThe data will be stored into DB...")
        break
    if answer == "c":
        print("\nAre you sure you want to terminate the session?"
              "All information will be lost.\n")
        while True:
            print("Enter 'a' to terminate, "
                  "'b' to go back to the previous options.")
            option = input("Your input: ").lower()
            if option == "a":
                print("\nBye.  Have a nice day!")
                exit()
            if option == "b":
                break
            else:
                print("\nInvalid entry.")
                continue
    else:
        # Let the user choose which item to update.
        while True:
            print("Select the item you need to correct.\n")
            print("a: First name")
            print("b: Last name")
            print("c: Bank")
            print("d: Deposit value in savings account")
            print("e: Deposit value in checking account")
            print("f: Go back to the previous options\n")
            choice = input("Enter a-f: ").lower()
            # Let the administrator make changes in the customer's information
            if choice == 'a':
                user.fname = collect_name("correct first name")
                break
            elif choice == 'b':
                user.lname = collect_name("correct last name: ")
                break
            elif choice == 'c':
                # Change the bank, so get a new user ID and account IDs.
                code = collect_bank_code()
                user.bank, user.user_id, new_accts = get_ids(code)
                user.svg_acct_id, user.check_acct_id = new_accts
                break
            elif choice == 'd':
                user.svg_dp = collect_val("Initial deposit in savings account: ")
                break
            elif choice == 'e':
                user.check_dp = collect_val("Initial deposit in checking account: ")
                break
            elif choice == 'f':
                break
            else:
                print("\nInvalid entry. Please try again.\n")
                continue
# Insert the data into DB.
create_new_accounts(user)


date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

salt = os.urandom(32)
pin = "111111"
key = hash_pin_with_salt(pin, salt)

user1 = User("John", "Smith", "John Smith", "North Bank", 100001, salt, key, 1100001, 1200001, '1000.00', '1000.00', date)
user2 = User("Katie", "Baker", "Katie Baker", "East Bank", 200001, salt, key, 2100001, 2200001, '1000.00', '1000.00', date)
user3 = User("Jamie", "Adams", "Jamie Adams", "South Bank", 300001, salt, key, 3100001, 3200001, '1000.00', '1000.00', date)

# create_new_accounts(user3)