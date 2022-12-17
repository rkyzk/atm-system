# General Introduction

This Python application provides a banking system. It offers a terminal for bank personnel to make accounts for their new customers, and a second terminal, an ATM terminal, where customers can carry out various transactions: they can 1)withdraw 2) deposit 3) transfer 4) view their balances 5) view transactions in the past 30 days.  The data are stored in three separate tables "Users," "Accounts," and "Transactions" in the database (SQLite). 

# ATM terminal (atm.py)

## Collecting user IDs
First the users will be asked to enter user IDs.  In real cases the machine will read off the IDs from the cards, so there should be no need to validate the values.  In this program, the users must type in their own IDs, so I prepared a validation system to accept only the IDs that are stored in the database.  If other values are entered, the system asks the user to enter valid IDs.

In the process above, I first test if the input consists of numbers only, since any inputs other than a number will cause an error when they are set as arguments for the “get_user_info” function.  If the input is a number, the system will obtain the user information through “get_user_info” function.  If the given IDs don’t exist in the database, the system will ask the users to reenter their IDs.

If the card has been deactivated, (if the flag is set to “s” – “s” for “suspended”), the system tells the users to call personnel  for assistance.  In that case the personnel can use “activate” function in sql.py to reactivate the card by setting the flag back to “a” (“a” for “active”).  

## Collecting passwords
Next the users will be prompted to enter their pin numbers.  With “validate_pin” function, the input will be hashed with the user’s salt value that is obtained from the database, and this key value will be compared with the key stored in the database.  If the new key matches the stored key, the system will print a message saying “Login Success.”  If not, the users will be asked to reenter their pin.  If they fail 4 times, the system will deactivate the card by setting the flag to “s” and terminate the program and let the users know these consequences.  

After a successful login, the users will be greeted by the system and will be asked to select the transaction they wish to undertake.  The options are:
a.	Withdraw
b.	Deposit
c.	Transfer
d.	View your account balances
e.	View recent transactions (from the past 30 days)
f.	Exit

A. Withdraw” 
The users are asked to enter the amount of withdrawal (should be given in multiples of 10, which will be validated via “collect_val” and “validate_val” functions.  Then “withdrawal” function will be called and the data will be updated.  The program will terminate if the given amount is greater than the balance in their account.

B. Deposit,” in real scenario, the users will insert money, and the machine should count the money.  In this program, the system asks the users to input the value manually. Again the system accepts only multiples of 10.  “deposit” function will be called, and the data will be updated.

C. Transfer” is selected, the users will input 
1) if the transfer should be made from their savings account or checking account
2) the recipient’s ID 
3) the amount of money to transfer 
4) transfer notes.  
They will be asked to reenter valid values if 
1)	the recipient’s ID is not found in the database
2)	the ID from which the users are making the transfer is selected
3)	empty strings or alphabets are entered for IDs or money values

Notes: The users can transfer money from their own checking account to their savings account, or vice versa.  
The money value should be input in the form of an integer or with values of cents (e.g. “50” or “50.00”

D. View your balances.
The system will obtain the balances of the user’s savings and checking account and displays the values in a table.  

E. View your transactions
The system will get a list of transaction records of the user from the previous 30 days.  With the use of a for loop, the items in the list will be sorted into the records of the savings account and those of the checking account.  And the records will be shown in separate tables.

F. Exit
The program will be terminated.  

After each transaction, the system asks the users if they want to make further transactions.  If yes, the users will be sent back to the selection of transactions.  If not, the program will be terminated.  

# Terminal for bank personnel (admin.py)
This terminal is for the bank personnel to create accounts for their new customers.  

First the users (here, the users refer to the bank personnel) will be greeted with a message “Hello!” and for clarity, the system ensures them that the terminal is for creating new accounts.  
The users will input:
1)	the customer’s first name
2)	the customer’s last name 
3)	which bank they are creating the accounts (North Bank, East Bank, or South Bank)
4)	initial deposit value in the savings account
5)	initial deposit value in the checking account
After item 3), the system will provide a user ID, savings account ID and checking account ID.  

## How user and account IDs are assigned:
User IDs have 6 digits.  The first number tells which bank the user belongs to. (1 for North Bank, 2 for East Bank and 3 for South Bank.)  The rest 5 digits are for identifying users.  For example, the first person to open accounts at North Bank will have a user ID of 100001, and the second person will get 100002 and so on.  Each time a new user ID will be assigned, the system will find the ID with the highest number that belongs to the selected bank in the database, and return the value added by 1.  

The account IDs have 7 digits.  The first number tells which bank the accounts belong to, just as user IDs, and the second number tells if the account is savings or checking account.  1 is for savings account, and 2 is for checking account.  For example 1100001 is an ID of a savings account at North Bank.  1200001 is an ID of a checking account at North Bank.  In a similar manner as user IDs, the system will search the IDs with the highest numbers belonging to the selected bank in the database, add them by 1 and return the values as account IDs.  Each customer will have unique user and account IDs.  

User and account IDs are stored in variables. 
Notes: All new customers will have both savings and checking accounts.

## Getting a pin, salt and hashing it.
A 6-digit pin will be generated through get_pin() function.  A salt to hash the pin will be also generated to hash the pin.  This will be stored as variable “key.”  (For security reason, the pin itself will not be stored in the database, but instead the key and the salt will be stored.  
When the bank customers enter their pin in order to log into the ATM system, the system will acquire the user’s salt value from the database, hash the entered pin and compare the resulting key with the key which was stored in the database.)  

In this program the system will print the pin so those who test the program can use it.
In real cases the pin will be shown only to the customer.  

The system gets one last variable date by calling now() function from datetime module.
All the information will be stored in class User object user.
The entered information will be printed for confirmation.  

If the users can choose to 
1)	insert the data as they are (then the data will be inserted into database), or
2)	choose to make changes
3)	to terminate the program (then they will be reminded that all data will be lost, and they will have decide if they really want to exit the program or continue.)
If they choose to make changes, they can change
1)	first name
2)	last name
3)	bank
4)	deposit in the savings account 
5)	checking account
6)	go back to previous options

According to what they select, they can enter correct values and then they will be asked to make further changes or insert the information in the database.  
Note, if they need to change the bank, then the user ID and account IDs will also be updated.  

When the users finish correcting the information, the data will be inserted to 3 tables: “Users,” “Accounts” and “Transactions.” 

Credits:


