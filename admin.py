from sql import * 
import decimal
D=decimal.Decimal
import random
from datetime import datetime
import hashlib
import os

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




print("****************************")
print("          Hello!")
print("****************************\n")
fname = input("Enter the customer's first name: ")
lname = input("Enter the customer's last name: ")
print("\nAt which bank are you creating accounts?")
print("Enter 'a' for North Bank\n'b' for East Bank\n'c' for South Bank.")
code = input("Your input: ")
svg_dp_str = input("\nInitial deposit in savings account: ")
check_dp_str = input("Initial deposit in checking account: ")

# Get a pin and salt and hash the pin to get a key
salt = os.urandom(32)
pin = get_pin()
key = hash_pin_with_salt(pin, salt)
# In real situations the pin will be shown only to the customer
# but here, it will be printed so testers can use it.
print(f"Pin: {pin}")
print(key) # remove this later
print(salt)  # remove this later

"""

#insert a sample user
date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

insert_user("John", "Smith", "North Bank", 100001, "salt", "key", 1100001, 120001)
insert_account(1100001, 100001, "John Smith", "North Bank", "savings", '1000.00')
insert_account(1200001, 100001, "John Smith", "North Bank", "checking", '1000.00')
insert_transaction(1100001, 100001, "deposit", "NA", "initial deposit", '1000.00', date)
insert_transaction(1200001, 100001, "deposit", "NA", "initial deposit", '1000.00', date)

insert_user("Mary", "Adams", "East Bank", 200001, "salt", "key", 2100001, 220001)
insert_account(2100001, 200001, "Mary Adams", "East Bank", "savings", '1000.00')
insert_account(2200001, 200001, "Mary Adams", "East Bank", "checking", '1000.00')
insert_transaction(2100001, 200001, "deposit", "NA", "initial deposit", '1000.00', date)
insert_transaction(2200001, 200001, "deposit", "NA", "initial deposit", '1000.00', date)

insert_user("Paul", "McLane", "South Bank", 300001, "salt", "key", 3100001, 320001)
insert_account(3100001, 300001, "Paul McLane", "South Bank", "savings", '1000.00')
insert_account(3200001, 300001, "Paul McLane", "South Bank", "checking", '1000.00')
insert_transaction(3100001, 300001, "deposit", "NA", "initial deposit", '1000.00', date)
insert_transaction(3200001, 300001, "deposit", "NA", "initial deposit", '1000.00', date)




"""
