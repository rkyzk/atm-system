import sqlite3
from datetime import datetime, timedelta
import decimal
from user_partial_info import UserPartialInfo
from user import User

#
to_decimal = decimal.Decimal

# Set SQL "Insert" queries for different tables into variables.
sql_insert_user = "INSERT INTO Users VALUES (:fname, :lname, :bank, :user_id, :salt, " \
                  ":key, :svg_acct_id, :check_acct_id, :flag)"

sql_insert_account = "INSERT INTO Accounts VALUES (:acct_id, :user_id, :holder, " \
                     ":bank, :acct_type, :balance)"

sql_insert_transaction = "INSERT INTO Transactions VALUES (:acct_id, :acct_type, " \
                         ":user_id, :trs_type, :trs_to_or_from, :trs_notes, " \
                         ":amount, :date)"

def create_table_users():
    """Create table "Users" for storing information of users."""
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        with conn:
            c.execute("""CREATE TABLE IF NOT EXISTS Users (
                fname text NOT NULL,
                lname text NOT NULL,
                bank text NOT NULL,
                user_id integer NOT NULL,
                salt text NOT NULL,
                key text NOT NULL,
                svg_acct_id integer NOT NULL,
                check_acct_id integer NOT NULL,
                flag text DEFAULT "a"
                )""")
    except Exception as e:
        print("There was an error.  The table wasn't created.")
        print(e)
        exit()
    finally:
        conn.close()

def create_table_accounts():
    """Create table "Accounts" for storing information accounts."""
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        with conn:
            c.execute("""CREATE TABLE IF NOT EXISTS Accounts (
                acct_id integer NOT NULL,
                user_id integer NOT NULL ,
                holder text NOT NULL,
                bank text NOT NULL,
                acct_type text NOT NULL,
                balance text NOT NULL
                )""")
    except Exception as e:
        print("There was an error.  The table wasn't created.")
        print(e)
        exit()
    finally:
        conn.close()

def create_table_transactions():
    """Create Table "Transactions" for storing transaction records."""
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        with conn:
            c.execute("""CREATE TABLE IF NOT EXISTS Transactions (
                acct_id integer NOT NULL,
                acct_type text NOT NULL,
                user_id integer NOT NULL,
                trs_type text NOT NULL,
                trs_to_or_from text NOT NULL,
                trs_notes text NOT NULL,
                amount text NOT NULL,
                date text NOT NULL
                )""")
    except Exception as e:
        print("There was an error.  The table wasn't created.")
        print(e)
        exit()
    finally:
        conn.close()

def print_with_linebreaks(list):
    """Print each item in the list in a new line"""
    for row in list:
        print(row)

def print_tables():
    """Print tables 'Users,' 'Accounts' and 'Transactions'"""
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("""SELECT fname, lname, bank, user_id, svg_acct_id,
                     check_acct_id, flag FROM Users""")
        print("Users")
        print_with_linebreaks(c.fetchall())
        c.execute("SELECT * FROM Accounts")
        print("-----------------------------")
        print("Accounts")
        print_with_linebreaks(c.fetchall())
        c.execute("SELECT * FROM Transactions")
        print("-----------------------------")
        print("Transactions")
        print_with_linebreaks(c.fetchall())
    except Exception as e:
        print("There was an error. The data couldn't be acquired.")
        print(e)
        exit()
    finally:
        conn.close()

def delete_tables():
    """Delete tables 'Users,' 'Accounts' and 'Transactions'"""
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        with conn:
            c.execute("DROP TABLE Users")
            c.execute("DROP TABLE Accounts")
            c.execute("DROP TABLE Transactions")
    except Exception as e:
        print("There was an error with the system."
              "The tables weren't deleted.")
        print(e)
        exit()
    finally:
        conn.close()

def get_user_id(code):
    """
    Get a list of existing user IDs of the selected bank
    and return the next available ID for that bank.
    """
    if code == "a":
        sql = "SELECT user_id FROM Users WHERE user_id LIKE '1%'"
        letter = "1"
    elif code == "b":
        sql = "SELECT user_id FROM Users WHERE user_id LIKE '2%'"
        letter = "2"
    else:
        sql = "SELECT user_id FROM Users WHERE user_id LIKE '3%'"
        letter = "3"
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute(sql)
        list = c.fetchall()
        # If list is None, return
        if list == []:
            return int("".join([letter, "000001"]))
        # Return the highest number of existing IDs added by 1.
        else:
            return max(list[0]) + 1
    except Exception as e:
        print("There was an error. User ID can't be acquired.")
        print(e)
        exit()
    finally:
        conn.close()

def get_acct_ids(code):
    """
    Get a list of savings and checking account IDs,
    find the highest number for both types of accounts
    and return the next available IDs (the highest existing numbers + 1).
    """
    if code == "a":
        # Store the prefixes of savings and checking account IDs of North Bank.
        sql_var = ["'11%'", "'12%'"]
        letter = "1"
    elif code == "b":
        # Do the same for East Bank
        sql_var = ["'21%'", "'22%'"]
        letter = "2"
    else:
        # Do the same for South Bank
        sql_var = ["'31%'", "'32%'"]
        letter = "3"
    new_accts = []
    # In the first round of the for loop below, store the next available
    # savings account ID.
    # In the second round, store the next available checking account ID.
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        for var in sql_var:
            sql = "SELECT acct_id FROM Accounts WHERE acct_id LIKE " + var
            c.execute(sql)
            list = c.fetchall()
            if list == []:
                break
            else:
                new_accts.append(int((max(list))[0]) + 1)
        if new_accts != []:
            return new_accts
        else:
            svg_acct_id = "".join([letter, "1000001"])
            check_acct_id = "".join([letter, "2000001"])
            return [int(svg_acct_id), int(check_acct_id)]
    except Exception as e:
        print("There was an error. Account IDs can't be acquired.")
        print(e)
        exit()
    finally:
        conn.close()

def set_user_values(user):
    values = {'fname': user.fname, 'lname': user.lname, 'bank': user.bank,
            'user_id': user.user_id, 'salt': user.salt, 'key': user.key,
            'svg_acct_id': user.svg_acct_id,
            'check_acct_id': user.check_acct_id, 'flag': 'a'}
    return values

def set_account_values(user, acct_id, balance):
    if str(acct_id)[1] == "1":
        values = {'acct_id': user.svg_acct_id, 'user_id': user.user_id,
                  'holder': " ".join([user.fname, user.lname]), 'bank': user.bank,
                  'acct_type': "savings", 'balance': balance}
    else:
        values = {'acct_id': user.check_acct_id, 'user_id': user.user_id,
                  'holder': " ".join([user.fname, user.lname]), 'bank': user.bank,
                  'acct_type': "checking", 'balance': balance}
    return values

def set_trans_values(acct_id, user_id, trs_type, trs_to_or_from,
                                trs_notes, amount, date):
    if str(acct_id)[1] == "1":
        values = {'acct_id': acct_id, 'acct_type': "savings",
                  'user_id': user_id, 'trs_type': trs_type,
                  'trs_to_or_from': trs_to_or_from,
                  'trs_notes': trs_notes, 'amount': amount, 'date': date}
    else:
        values = {'acct_id': acct_id, 'acct_type': "checking",
                  'user_id': user_id, 'trs_type': trs_type,
                  'trs_to_or_from': trs_to_or_from,
                  'trs_notes': trs_notes, 'amount': amount, 'date': date}
    return values

def create_new_accounts(user_info):
    """
    For a new customer, insert user information into table "Users."
    Insert new accounts information into table "Accounts."
    Insert new transaction records into table "Transactions."

    argument:
    user_info
    """
    # Get the current date and time.
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Get the bank name, user ID, account IDs and store them
    # in the following variables.
    bank = get_bank(user_info.bank_code)
    user_id = get_user_id(user_info.bank_code)
    svg_acct_id, check_acct_id = get_acct_ids(user_info.bank_code)
    # Insert all information into "User" class object "user."
    user = User(user_info.fname, user_info.lname, bank, user_id,
                user_info.salt, user_info.key, svg_acct_id,
                check_acct_id, 'a')
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute('Begin')
        # Insert user information to table "Users."
        c.execute(sql_insert_user, set_user_values(user))
        # insert savings account information into table "Accounts"
        values = set_account_values(user, svg_acct_id, user_info.svg_dp)
        c.execute(sql_insert_account, values)
        # Insert checking account information into table "Accounts."
        values = set_account_values(user, check_acct_id, user_info.check_dp)
        c.execute(sql_insert_account, values)
        # Insert the record of the deposit into the savings account
        # into table "Transactions."
        amount = "".join(["+", user_info.svg_dp])
        values = set_trans_values(svg_acct_id, user_id,
                                  "deposit", "NA", "NA", amount, date)
        c.execute(sql_insert_transaction, values)
        # Insert the record of the deposit into the checking account
        # into table "Transactions."
        amount = "".join(["+", user_info.check_dp])
        values = set_trans_values(check_acct_id, user_id,
                                  "deposit", "NA", "NA", amount, date)
        c.execute(sql_insert_transaction, values)
        conn.commit()
        print("The data have been stored in the database.")
    except Exception as e:
        if conn:
            conn.rollback()
        print("There was an error.  The data haven't been inserted."
              "Please try again.")
        print(e)
        exit()
    finally:
        conn.close()

def get_user_info(user_id):
    """
    Get user Info of the given user ID.

    :argument: user_id: user ID
    :return: user info of the given user ID, or "None" if there's no data with the ID.
    :rtype: User or None
    """
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Users WHERE user_id = " + str(user_id))
        info_db = c.fetchone()
        # Insert all info into class "User" object "user"
        if info_db is None:
            return None
        else:
            user = User(info_db[0], info_db[1], info_db[2], info_db[3],
                        info_db[4], info_db[5], info_db[6], info_db[7],
                        info_db[8])
            return user
    except Exception as e:
        print("There was an error. "
              "The user information couldn't be acquired.")
        print(e)
        exit()
    finally:
        conn.close()

def deactivate(user_id):
    """
    Prevent the user with the given ID from logging into
    the ATM system by setting the flag to "s" ("s" for "suspended").
    """
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("UPDATE Users SET flag = 's' WHERE user_id = "
                  + str(user_id))
        conn.commit()
        print("The card has been deactivated. Please call the number "
              "on the back of your card for assistance.")
    except Exception as e:
        if conn:
            conn.rollback()
        print("There was an error with the system.")
        print(e)
        exit()
    finally:
        conn.close()

def activate(user_id):
    """
    Activate the card by setting the flag value back to
    "a" ("a" for "active").
    """
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute('Begin')
        c.execute("UPDATE Users SET flag = 'a' WHERE user_id = "
                  + str(user_id))
        conn.commit()
        message = "The card has been activated."
        return message
    except Exception as e:
        if conn:
            conn.rollback()
        print("There was an error. The user card couldn't be activated.")
        print(e)
        exit()
    finally:
        conn.close()

def withdraw(amount, user):
    """
    Get the balance of the user from table "Accounts."
    If the balance is greater than "amount,"
    subtract it by "amount" and set the new balance to
    "balance" in table "Accounts."

    arguments:
    amount -- amount of money to withdraw
    user -- the user information
    """
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        # Get the balance of the user.
        c.execute("SELECT balance FROM Accounts WHERE acct_id = "
                  + str(user.check_acct_id))
        old_balance = c.fetchone()
        # If the old balance is less than "amount," print
        # the following message and terminate the program.
        if to_decimal(old_balance[0]) < to_decimal(amount):
            print("No sufficient money in the account."
                  "The session will be terminated.")
            exit()
        else:
            # Calculate the new balance.
            new_balance = (to_decimal(old_balance[0]) - to_decimal(amount))
            # Get the current date and time.
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Update the balance in table "Accounts."
            c.execute('Begin')
            c.execute("UPDATE Accounts SET balance = '" + str(new_balance)
                      + "' WHERE acct_id = " + str(user.check_acct_id))
            # Insert the record of this transaction into table
            # "Transactions."
            amt_with_sign = "".join(["-", amount])
            values = set_trans_values(user.check_acct_id, user.user_id,
                                            "withdrawal", "NA", "NA",
                                            amt_with_sign, date)
            c.execute(sql_insert_transaction, values)
            conn.commit()
            print(f"\n${amount} has been withdrawn from your checking"
                  f"account.\nPlease take your money and card.")
    except Exception as e:
        # In case of an error, roll back if there's a connection,
        # print an error message and terminate the program.
        if conn:
            conn.rollback()
        print("There was an error. Withdrawal is not possible at this time."
              "Please try again.")
        print(e)
        exit()
    finally:
        conn.close()

def deposit(amount, check_acct_id, user_id):
    """
    Get the balance of the user from table "Accounts."
    Add "amount" to the balance, update the balance
    and insert the record into table "Transactions."
    """
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        # Get the balance of the user.
        c.execute("SELECT balance FROM Accounts WHERE acct_id = "
                  + str(check_acct_id))
        old_balance = c.fetchone()
        # Calculate the new balance.
        new_balance = D(old_balance[0]) + D(amount)
        # Update the balance in table "Accounts."
        c.execute('Begin')
        c.execute("UPDATE Accounts SET balance = '" + str(new_balance)
                  + "' WHERE acct_id = " + str(check_acct_id))
        # Get the current date and time.
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Insert the record of the transaction into table "Transactions."
        c.execute("INSERT INTO Transactions VALUES ("
                  ":acct_id, :acct_type, :user_id, :trs_type, "
                  ":trs_to_or_from, :trs_notes, :amount, :date"
                  ")",
                  {'acct_id': check_acct_id, 'acct_type': "checking",
                   'user_id': user_id, 'trs_type': "deposit",
                   'trs_to_or_from': "NA", 'trs_notes': "NA",
                   'amount': "+" + amount, 'date': date})
        conn.commit()
        print(f"${amount} has been added to your checking account.")
    except Exception as e:
        # In case of an error, roll back if there's a connection,
        # print an error message and terminate the program.
        print("There was an error.  Deposit is not possible at this time."
              "  Please try again.")
        print(e)
        if conn:
            conn.rollback()
        exit()
    finally:
        conn.close()

def get_recip_info(recip_acct_id):
    """
    Get the user ID and the full name of the customer
    with the given account ID and return the information.
    """
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        # Get the recipient's user ID and name from table "Accounts."
        c.execute("SELECT user_id, holder FROM Accounts WHERE acct_id = "
                  + recip_acct_id)
        recip = c.fetchone()
        return recip
    except Exception as e:
        # In case of an error, roll back if there's a connection,
        # print an error message and terminate the program.
        print("There was an error.  The recipient's information couldn't "
              "be acquired.")
        print(e)
        exit()
    finally:
        conn.close()

def transfer(name, user_id, acct_id, acct_type, amount,
             recip, recip_user_id, trs_notes, recip_acct_id
             ):
    """
    Get the balance of the sender. If the balance is greater than "amount,"
    subtract "amount" from the balance, update the account information
    and the transaction history.
    Also get the balance of the recipient.  Add "amount" value to the balance,
    update the account information and transaction history of the recipient.
    """
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        # Get the balance of the sender.
        c.execute("SELECT balance FROM Accounts WHERE acct_id = "
                  + str(acct_id))
        old_balance = c.fetchone()
        # Calculate the new balance.
        new_balance = D(old_balance[0]) - D(amount)
        # If the sender doesn't have enough money in the account,
        # print the message below and terminate the program.
        if new_balance < 0:
            print("You don't have sufficient money in your account to "
                  "make this transfer.\nThe program will be terminated.")
            exit()
        else:
            new_balance = D(old_balance[0]) - D(amount)
            c.execute('Begin')
            # Update the sender's new balance.
            c.execute("UPDATE Accounts SET balance = '" + str(new_balance)
                      + "' WHERE acct_id = " + str(acct_id))
            # Add the record to table "Transactions."
            trs_type = "transfer sent"
            trs_to_or_from = " ".join(["to", recip])
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO Transactions VALUES ("
                      ":acct_id, :acct_type, :user_id, :trs_type, "
                      ":trs_to_or_from, :trs_notes, :amount, :date"
                      ")",
                      {'acct_id': acct_id, 'acct_type': acct_type,
                       'user_id': user_id, 'trs_type': trs_type,
                       'trs_to_or_from': trs_to_or_from,
                       'trs_notes': trs_notes, 'amount': "-" + amount,
                       'date': date})
            # Get the balance of the recipient.
            if str(acct_id)[1] == "1":
                acct_type = "saving"
            else:
                acct_type = "checking"
            c.execute("SELECT balance FROM Accounts WHERE acct_id = "
                      + recip_acct_id)
            old_balance = c.fetchone()
            # Calculate the new balance of the recipient.
            new_balance = D(old_balance[0]) + D(amount)
            # Update the recipient's new balance.
            c.execute("UPDATE Accounts SET balance = '" + str(new_balance)
                      + "' WHERE acct_id = " + recip_acct_id)
            # Add the record to table "Transactions."
            trs_type = "transfer received"
            trs_to_or_from = " ".join(["from", name])
            c.execute("INSERT INTO Transactions VALUES ("
                      ":acct_id, :acct_type, :user_id, :trs_type,"
                      " :trs_to_or_from, :trs_notes, :amount, :date"
                      ")",
                      {'acct_id': int(recip_acct_id), 'acct_type': acct_type,
                       'user_id': recip_user_id, 'trs_type': trs_type,
                       'trs_to_or_from': trs_to_or_from,
                       'trs_notes': trs_notes, 'amount': "+" + amount,
                       'date': date})
            conn.commit()
            print("\nThe money has been transferred.")
    except Exception as e:
        # In case of an error, roll back if there's a connection,
        # print an error message and terminate the program.
        if conn:
            conn.rollback()
        print("\nThere was an error.  Transfer is not possible "
              "at this time.")
        print(e)
        exit()
    finally:
        conn.close()

def get_balances(user_id):
    """
    Get the balance of the savings and checking accounts
    of the user.
    """
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("SELECT acct_id, balance FROM Accounts WHERE user_id = "
                  + str(user_id))
        list = c.fetchall()
        return list
    except Exception as e:
        # In case of an error, roll back if there's a connection,
        # print an error message and terminate the program.
        print("\nThere was an error.  The data couldn't be acquired.")
        print(e)
        exit()
    finally:
        conn.close()


def get_transactions(user_id):
    """
    Get transaction records of the user
    in the past 30 days.
    """
    # Get the date time of 30 days ago in string.
    start_datetime = datetime.now() - timedelta(days=30)
    start_date_str = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        # Select the transaction records of the user in the past 30 days
        # and return the list.
        c.execute("SELECT acct_id, acct_type, date, trs_type, "
                  "trs_to_or_from, trs_notes, amount FROM Transactions "
                  "WHERE user_id = " + str(user_id) + " AND date >= '"
                  + start_date_str + "'")
        list = c.fetchall()
        return list
    except Exception as e:
        # In case of an error, roll back if there's a connection,
        # print an error message and terminate the program.
        print("There was an error. The information couldn't be acquired.")
        print(e)
        exit()
    finally:
        conn.close()

def update():                # cut this part later
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("UPDATE Transactions SET user_id = 200001 "
              "WHERE amount = '+10.00'")
    conn.commit()
    conn.close()

#create_table_accounts()
#create_table_users()
#create_table_transactions()
#print_tables()