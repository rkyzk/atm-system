
"""This module contains program for bank personnel to insert information
of new customers and their accounts into database."""

from user_partial_info import UserPartialInfo
from functions import *
import os
import time

print("****************************")
print("          Hello!")
print("****************************\n")
print("This terminal is for creating new accounts.\n")
time.sleep(1.5)
# Collect the customer's first name and validate it.
fname = collect_name("Enter the customer's first name: ")
# Collect the customer's first name and validate it.
lname = collect_name("Enter the customer's last name: ")
# The customer's full name.
holder = " ".join([fname, lname])
# Have the user select a bank.
print("\nAt which bank are you creating accounts?")
# Get the bank code
bank_code = collect_bank_code()
# Input initial deposit values for each account.
svg_dp = collect_mult_of_10("Enter initial deposit in savings account: ")
check_dp = collect_mult_of_10("Enter initial deposit in checking account: ")
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
    answer = input("Enter 'a', 'b' or 'c': ").lower()
    if answer not in ['a', 'b', 'c']:
        print("\nInvalid entry.  Please try again.")
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
            option = input("Your input: ").lower()
            if option == "a":
                print("\nBye.  Have a nice day!")
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
            choice = input("Enter a-f: ").lower()
            # Let the user make changes in the customer's information.
            if choice == 'a':
                fname = collect_name("Enter the customer's "
                                     "correct first name: ")
                break
            if choice == 'b':
                lname = collect_name("Enter the customer's "
                                     "correct last name: ")
                break
            if choice == 'c':
                bank_code = collect_bank_code()
                break
            if choice == 'd':
                svg_dp = collect_mult_of_10("Enter initial deposit in "
                                            "savings account in "
                                            "a multiple of 10: ")
                break
            if choice == 'e':
                check_dp = collect_mult_of_10("Enter initial deposit in "
                                              "checking account in "
                                              "a multiple of 10: ")
                break
            if choice == 'f':
                break
            else:
                print("\nInvalid entry. Please try again.")
# Store all user info in a User class object named "user."
user_partial_info = UserPartialInfo(fname, lname, bank_code, salt, key,
                                    svg_dp, check_dp)
# Insert the data into DB.
user_id = create_new_accounts(user_partial_info)
# Print IDs and balances of accounts
list_balances = get_balances(user_id)
print(f"Name: {fname} {lname}")
print(f"User ID: {user_id}")
print(f"Savings Account ID: {list_balances[0][0]}")
print(f"Balance: ${list_balances[0][1]}")
print(f"Checking account ID: {list_balances[1][0]}")
print(f"Balance: ${list_balances[1][1]}\n")
