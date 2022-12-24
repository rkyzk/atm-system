"""This modle holds functions that are used in the banking system,
both in atm.py and admin.py"""
import random
import hashlib
from sql import *

#-----------   Functions used both in atm.py and admin.py modules ----#
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

#-----------   Functions used in admin.py.   --------------#
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

def collect_name(f_lname):
    """
    Print prompt message and collect the customer's name.
    If the input contains only alphabet, return the name as is.
    If not, prompt the user to reenter the name.

    :argument: f_lname: prompt message asking for first/last name
    :return: validated name
    :rtype: str
    """
    while True:
        name = input(f_lname).replace(" ", "")
        if name.isalpha():
            return name
        else:
            print("Invalid entry (enter only alphabets).")

def collect_bank_code():
    """Have the user select the bank and return the code.

    :return: code: bank code
    :rtype: str
    """
    while True:
        print("Enter 'a' for North Bank\n'b' for East Bank\n"
              "'c' for South Bank.")
        code = input("Your input: ").lower().replace(" ", "")  # The bank code
        if code in ["a", "b", "c"]:
            return code
        else:
            print("\nInvalid entry.")

def get_bank(code):
    """
    Return the bank name for the given code.

    :argument: code: bank code
    :return: bank: bank name
    :rtype: str
    """
    if code == "a":
        bank = "North Bank"
    elif code == "b":
        bank = "East Bank"
    else:
        bank = "South Bank"
    return bank

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

def print_data(fname, lname, bank_code, svg_dp, check_dp):
    """Print the information of the given user.

    :argument: fname: first name
               lname: last name
               bank_code: bank code
               svg_dp: deposit value in savings account
               check_dp: deposit value in checking account
    """
    print(f"Name: {fname} {lname}")
    print(f"Bank Name: {get_bank(bank_code)}")
    print(f"--Initial Deposits--")
    print(f"Savings Account: ${svg_dp}")
    print(f"Checking Account: ${check_dp}\n")

#-----------   Functions used in atm.py.   --------------#
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

#-----------   Functions used in atm.py.   --------------#
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

