from sql import * 
import decimal
D=decimal.Decimal
from datetime import datetime

"""
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
"""
#insert a sample user
date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

insert_user("John", "Smith", "North Bank", 100001, "salt", "key", 1100001, 1200001)
insert_account(1100001, 100001, "John Smith", "North Bank", "savings", D('1000.00'))
insert_account(1200001, 100001, "John Smith", "North Bank", "checking", D('1000.00'))
insert_transaction(1100001, 100001, "deposit", "NA", "initial deposit", "1000.00", date)
insert_transaction(1200001, 100001, "deposit", "NA", "initial deposit", "1000.00", date)







