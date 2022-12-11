import sqlite3

"""
Create table "Users" to store information of users.

fname -- first name
lname -- last name
bank -- bank name
"""
def create_table_users():
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
    finally:
        conn.close()

"""
Create Table "Accounts" to store information accounts.
"""
def create_table_accounts():
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
                balance decimal NOT NULL
                )""")
    except Exception as e:
        print("There was an error.  The table wasn't created.")
        print(e)
    finally:
        conn.close()

"""
Create Table "Transactions" to store transaction records.
"""
def create_table_transactions():
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        with conn:
            c.execute("""CREATE TABLE IF NOT EXISTS Transactions (
                acct_id integer NOT NULL,
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
    finally:
        conn.close()

def print_tables():
    conn = sqlite3.connect('bank.db')  
    c = conn.cursor()
    c.execute("""SELECT * FROM Users""")
    print("Users")
    print(c.fetchall())
    c.execute("""SELECT * FROM Accounts""")
    print("-----------------------------")
    print("Accounts")
    print(c.fetchall())
    c.execute("""SELECT * FROM Transactions""")
    print("-----------------------------")
    print("Transactions")
    print(c.fetchall())
    conn.close()

#create_table_users()
#create_table_accounts()
#create_table_transactions()
print_tables()

def withdraw(user_id, amount):
    pass

def deposit(amount, acct_id):
    pass

def transfer(user_id, amount, recip_acct_id, trs_notes):
    pass

def display_balance(user_id):
    pass

def display_transactions(user_id):
    pass