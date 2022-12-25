"""This modle holds functions that are used in the banking system,
both in atm.py and admin.py"""
import random
import hashlib
from user import User
from sql import *

# -----------   Functions used both in atm.py and admin.py modules ----


def collect_mult_of_10(msg):
    """
    Print the content of "msg" and prompt users to enter a value.
    If the input is a multiple of 10, add two decimal digits ".00"
    and return the value.
    :argument: msg: prompt message
    :returns: validated value added with two decimal digits ".00"
    :rtype: str
    """
    while True:
        value = input(msg)
        if value.isdigit() and value not in ["", "0"] and value.endswith("0"):
            decimal_val = ".".join([value, "00"])
            return decimal_val
        else:
            print("\nInvalid entry.")

# -----------   Functions used in admin.py.   --------------


def validate_admin_pass(username, password):
    pass

def get_pin():
    """Generate a random 6-digit pin and return it.

    :return: pin: pin number
    :rtype: str
    """
    str_pin = ""
    for n in range(6):
        str_pin += str(random.randrange(10))
    return str_pin


def hash_pin_with_salt(pin, salt):
    """Hash the pin with a given salt and return the key.

    :argument: pin
               salt
    :return: key
    :rtype: str
    """
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
        code = input("Your input: \n").lower()  # The bank code
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

# -----------   Functions used in atm.py.   --------------


def validate_pin(user_id, unhashed):
    """
    Get the salt and the stored key for the given user ID from the database,
    hash the argument "unhashed," and compare the new key with the stored key.
    Return "True" if they are identical, otherwise return "False."

    :arguments: user_id: user ID
                unhashed: pin that was entered by the user
    :return: True or False
    :rtype: boolean
    """
    user = get_user_info(user_id)
    salt = user.salt
    new_key = hashlib.pbkdf2_hmac('sha256', unhashed.encode('utf-8'),
                                  salt, 100000, dklen=128)
    if new_key == user.key:
        return True
    else:
        return False


def check_id(msg, length):
    """
    Prompt the users to enter a number and check if the input
    is a whole number with the specified number of digits
    starting with bank code 1, 2 or 3.

    :param msg: prompt message
    :param length: the number of digits
    :return: the validated number
    :rtype: str
    """
    while True:
        id = input(msg)
        if id.isdigit() and len(id) == length:
            if id[0] in ["1", "2", "3"]:
                return id
        else:
            print("Please enter a valid ID.")


def validate_val(val):
    """
    Return "True" if the argument "val" is a non-zero
    whole number or a positive number with two decimal digits.
    (e.g. '50' or '50.00')

    :argument: val: value to be validated
    :return: True or False
    :rtype: boolean
    """
    if val in ["0", "0.00"]:
        print("Please enter a non-zero value.")
        return False
    elif val.isdigit():
        return True
    elif len(val) < 4:
        return False
    elif val[-3] == "." and val[:-3].isdigit() and val[-2:].isdigit():
        return True
    else:
        return False


def collect_val(msg):
    """
    Print "msg" and have the users input a value and validate it
    with "validate_transfer_val" function.  If "False" is returned,
    prompt them to reenter a valid value.
    Otherwise, if the input "value" is an integer,
    add two decimal digits ".00" and return the value.  If "value"
    already has two decimal digits, return it as is.

    :argument: msg: prompt message
    :returns: validated value as is, or added with two decimal digits ".00"
    :rtype: str
    """
    while True:
        value = input(msg)
        if validate_val(value):
            if value.isdigit():
                decimal_val = value + ".00"
                return decimal_val
            else:
                return value
        else:
            print("Invalid entry.  Enter values with or without "
                  "number of cents (e.g. '50' or '50.00').")


def display_with_spaces(item_list):
    """
    Print items in the argument "list" with the numbers of spaces
    indicated in "list_num."
    :argument: item_list: a record in transaction history
    """
    list_num = [25, 20, 30, 35, 10]
    str = ""
    for n, item in enumerate(item_list):
        space = " "
        num = list_num[n] - len(item)
        str = "".join([str, item + space*num])
    print(str)


def print_row(transaction_list):
    """
    Using "display_with_spaces" function,
    print each row in the argument "list."

    :argument: transaction_list: list of transactions
    """
    for item in transaction_list:
        display_with_spaces(item)


def validate_len(length):
    """
    Have the users input notes and check the length.
    If the length is equal to or less than 35 characters,
    return the input.  Otherwise prompt them to reenter notes.

    :argument: length: max number of characters in trsfer notes
    :return: trs_notes: transfer notes
    :rtype: str
    """
    while True:
        trs_notes = input(f"Enter transfer notes (optional, "
                          f"max {length} characters): \n")
        if len(trs_notes) <= length:
            return trs_notes
        else:
            print(f"\nYou entered more than {length} characters.")
