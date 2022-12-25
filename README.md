# General Overview of Banking System Application

Banking System Application is a Python terminal application.  It offers a terminal for bank personnel to make accounts for new customers as well as a second terminal, an ATM terminal, where users can make various imaginary transactions: withdrawals, deposits, transfers, viewing their balances and viewing recent transactions.  The data of the customers, accounts and transactions are stored in three separate tables named “Users,” “Accounts” and “Transactions” respectively in SQLite3 database. 

## Terminal for Bank Personnel (admin.py)
### What users can do
- At this terminal the bank personnel can create accounts for their new customers.  

- First the users (or bank personnel) will be greeted with a message “Hello!” and for clarity, the system ensures them that the terminal is for creating new accounts.  

- The users will input:
1. the customer’s first name
2. the customer’s last name 
3. which bank they are creating accounts (North Bank, East Bank, or South Bank)
4. initial deposit value in the savings account
5. initial deposit value in the checking account

- Note: Every customer will have a savings account and a checking account.

### Getting a pin, salt and hashing it.
- A 7-digit pin will be randomly generated.  
- A salt to hash the pin will also be generated.  
- The hashed pin will be stored in variable “key.”
- For security reason, the pin itself will not be stored in the database, but instead the key and the salt will be stored.
- (When customers enter their pin in order to log into the ATM system, the system will acquire the user’s salt value from the database, hash the entered pin and compare the resulting key with the key which was stored in the database.)  
- In this program the system will print out the pin so checkers can test the program.
- In real scenario the pin will be shown only to the customer.  

### Confirming the data and storing them.
- The entered information will be printed out for confirmation.  
- The users can choose to 
1. insert the data as they are (then the data will be inserted into database), or
2. choose to make changes
3. to terminate the program 

- If they choose to make changes, they can change the customer’s:
1. first name
2. last name
3. bank
4. deposit in the savings account 
5. deposit in the checking account

- Users can correct the information, and the updated data will be displayed once again for confirmation.  
- They can choose to insert the data into database or make further changes.

### How user and account IDs are assigned:
When bank personnel decides to go ahead and insert the new customer’s information into the database, the system will assign user ID as well as account IDs.  
User IDs have 7 digits.  The first number tells which bank the customer belongs to.  (‘1’ indicates North Bank; ‘2’: East Bank; ‘3’: South Bank.)  The rest 6 digits are for identifying customers.  For example, the first person to open accounts at North Bank will have a user ID of 1000001, and the second person will have user ID of 100002 and so on. For each new customer, the system will search for the ID with the highest number among existing IDs of the selected bank, add 1 to the number and assign the value to the new customer.

The account IDs have 8 digits.  The first number tells which bank the accounts belong to, just as user IDs, and the second number tells if the account is savings or checking account.  ‘1’ indicates savings account, and ‘2’ indicates checking account.  For example, 11000001 is an ID of a savings account at North Bank.  12000001 is an ID of a checking account at North Bank.  In a similar manner to user IDs, for a new customer, the system will search for the ID with the highest number among existing IDs, add 1 to the value and assign the value to the new customer. 

Each customer will have unique user and account IDs.  

### Inserting Data
- The information will be stored in three tables in the database:  
- Information of users at all three banks will be stored in table “Users.” 
- Information of all accounts will be stored in table “Accounts.” 
- Information of all transaction records that take place in the accounts will be stored in table “Transactions.” 

### Printing user and account IDs
After the data have been successfully inserted, the system will print out the name of the customer, user ID, account IDs and the balances of the accounts.

## How to use the ATM terminal (atm.py)

### Collecting user ID and pin
- First users will be asked to enter their user IDs and a pin.  In real setting, the machine will read off the IDs from the cards, so there should be no need to validate the IDs.  But in this program, the users must type in their own IDs, so I prepared a validation system to accept only the IDs that are stored in the database.
- Then the users enter their pin, and the combination of the user ID and the pin will be validated.
-If they get the pin wrong 4 times, then the flag value of that user will be changed from “a” to “s” (“a” for “active; “s” for “suspended”) in table “Users.”
- If the flag value is set to “s, ” the user will be deterred from logging into the system.  
- In that case bank personnel can use “activate” function in sql.py to reactivate the card by setting the flag back to “a.”  
- After a successful login, the users will be greeted by the system and will be asked to select the transaction they want to make.  The options are:
a.  Withdraw
b.  Deposit
c.  Transfer
d.  View the account balances
e.  View recent transactions (from the past 30 days)
f.  Exit

A. Withdraw
- Users are asked to enter the amount they want to withdraw in a multiple of 10.
- If the requested withdrawal amount is greater than the balance in their account, the system will tell the customers that there isn’t sufficient money for the transaction, and the program will be terminated.  
- Otherwise the new balance will be calculated by subtracting the withdrawal amount from the old balance.
- The balance will be updated, and the transaction record will be added to the database.  

B. Deposit
- In real scenario, users will insert money, and the machine will count the value of deposit.  In this program, the system asks the users to input the value manually. 
- The new balance will be calculated and will be updated in the database, and the transaction record will be added as well.

C. Transfer
- Users will input:
1. whether they are making the transfer from their savings account or checking account
2. the recipient’s account ID 
3. the amount of money to transfer 
4. transfer notes (optional, max 35 characters)

- They will be asked to reenter valid values if 
1. the recipient’s ID is not found in the database
2. the account ID from which the user wants to make the transfer is entered as recipient’s ID
3. empty strings or non-numeric values are entered as transfer amount

- The program will be terminated, if the specified account of the sender doesn’t have sufficient money for the transfer.

- Notes: Users can transfer money from their own checking account to their savings account, and vice versa.  
The money value should be entered in the form of an integer or with values of cents (e.g. “50” or “50.00”)

D. View your balances
- The system will obtain the balances of the user’s savings and checking accounts and will display the values in a table.  

E. View your transactions
- The system will get a list of transaction records of the user from the previous 30 days.  The transaction histories of savings and checking accounts will be shown in separate tables.

*Notes for checkers: I added transaction records dating from more than 30 days ago to account ID 32000001 in order to test if the program to select only the records in the past 30 days functions well.  (By calling function print_tables() in sql.py, all records in the tables will be displayed.)*

F. Exit
- The program will be terminated.  

Lastly, after each transaction, the system asks the users if they want to make further transactions.  Until they decide to exit the program, they can continue to make transactions.

*Another note for checkers: I added one user at each bank, user_ID: 1000001, 2000001 and 3000001 for test purpose.  The pin number is 111111 for all three users.*

## Notes on functions.py and sql.py
I placed functions that make connections to database in sql.py and other functions in functions.py. 
sql.py contains a function print_tables(), which is not necessary for the function of the application but is useful while checking the system.

## Notes on class User and class UserPartialInfo
"UserPartialInfo" is a class that can host user information that will be collected by bank personnel and will be sent as argument of function “create_new_accounts.”  This class doesn’t hold the user and account IDs.  

Class "User" is a class containing variables that correspond to the variables stored in table “Users,” so it is used while inserting into and getting information from the database. 

## Future features:
- Currently I limited the length of transfer notes to 35 characters so the table of transaction history will not be distorted.  In the future, I will find a way to accommodate longer texts with line breaks in the column.  
- I will make a login system for bank personnel with a username and pin validation.
- I will add a program to reset pin numbers in case customers forget their pins.

# Testing:
- I passed the code through CI Python Linter and confirmed there are no problems.
- I tested all possible input options and confirmed that the interaction between the system and the users flow well.
- I tested that if users enter invalid inputs, (such as characters, an empty string, spaces or 0 where a non-zero number is expected.) the system will ask the users to reenter a valid value.  
- I tested that all prompt messages are clear and that there’s no confusion for users as to how to use the program.  

## Bugs:
Earlier, in “admin.py,” I assigned user and account IDs right after the bank has been selected.  I realized later that this might cause the same IDs to be assigned to multiple customers in case another bank personnel uses the terminal to serve a different customer at the same time.  I fixed the issue by letting the system assign user and account IDs right before inserting data into the database.  

## Validator Testing: 
No errors were returned from https://pep8ci.herokuapp.com

## Deployment
This project was deployed using Code Institute's mock terminal for Heroku.
- Steps to deploy:
1. Fork or clone the repository
2. Create a new Heroku app
3. Set the buildpacks to Python and NodeJS in the order
4. Link the Heroku app to the repository
5. Click on Deploy

## Credits:
The code to hash the pin with salt was taken from the following site:

[How To Hash Passwords In Python]https://nitratine.net/blog/post/how-to-hash-passwords-in-python/

The section in this readme file "Deployment" was taken from the readme file of Love Sandwiches Project by Code Institute.