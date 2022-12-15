from sql import *
import hashlib

def validate_pin(user_id, unhashed):
    user = get_user_info(user_id)
    salt = user[4]
    new_key = hashlib.pbkdf2_hmac('sha256', unhashed.encode('utf-8'), salt, 100000, dklen=128)
    if new_key == user[5]:
        return True
    else:
        return False

# In a real setting, the user will insert their card,
# and the machine will read off their user_ID, but here,
# we'll have the user input their ID and pin.
# If they get it wrong 4 times, the card will be deactivated.
n = 0
while n < 4:
    user_id = input("Enter your user ID: ")
    unhashed = input("Enter your pin: ")
    user = get_user_info(int(user_id))  # indent----------?
    if user == None:
        print("The user ID or the pin is wrong.  Please try again.")
        n += 1
        continue
    # if the card has been deactivated (then it has a flag value of "s" in Table Users.)
    # tell the user to call personnel.
    if user[8] == "s":
        print("Your card has been suspended.\nPlease call "
              "the number on the back of your card for assistance.")
        exit()
    elif validate_pin(user_id, unhashed):
        print('\nLogin Success\n')
        break
    else:
        print("The user ID or the pin is wrong.  Please try again.")
        n += 1
else:
    # After 4 wrong entries, block further login attempts by changing the flag to 's' in DB
    deactivate(user_id)   # (user)id can't be empty
    print("The card has been deactivated. Please call the number\
        on the back of your card for assistance.")
    exit()

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
            amount = input('Enter the amount you wish to withdraw: ')
            withdraw(user_id, amount)
            print("Please take the money and your card.")
            break
        if choice == "b":
            # In real settings the user will insert money, and the machine will
            # count the inserted money, but here, let the user enter the deposit value.
            amount = input('Enter the amount of money you are depositing: ')
            deposit(amount, acct_id)
            print(f"${amount} was depositted to your account.")
            break
        if choice == "c":
            recip_acct_id = input("Enter the recipient's account number: ")
            amount = input("The amount to transfer: ")
            trs_notes = input("Enter transactions notes(optional): ")
            transfer(user_id, amount, recip_acct_id, trs_notes)
            print(f"${amount} was transferred to {recip_acct_id}.")
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