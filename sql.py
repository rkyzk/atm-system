import sqlite3
import decimal
D=decimal.Decimal

from datetime import datetime

def adapt_decimal(d):
    return str(d)

def convert_decimal(s):
    return decimal.Decimal(s.decode('utf-8'))

# Register the adapter
sqlite3.register_adapter(D, adapt_decimal)

# Register the converter
sqlite3.register_converter("decimal", convert_decimal)

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
                balance text NOT NULL
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

def print_with_linebreaks(list):
    for row in list:
        print(row)

def print_tables():
    conn = sqlite3.connect('bank.db')  
    c = conn.cursor()
    c.execute("""SELECT * FROM Users""")
    print("Users")
    print_with_linebreaks(c.fetchall())
    c.execute("""SELECT * FROM Accounts""")
    print("-----------------------------")
    print("Accounts")
    print_with_linebreaks(c.fetchall())
    c.execute("""SELECT * FROM Transactions""")
    print("-----------------------------")
    print("Transactions")   
    print_with_linebreaks(c.fetchall())
    conn.close()

def delete_tables():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    with conn:
        c.execute("""DROP TABLE Users""")
        c.execute("""DROP TABLE Accounts""")
        c.execute("""DROP TABLE Transactions""")
    conn.close()

def insert_user(fname, lname, bank, user_id, salt, key, svg_acct_id, check_acct_id):
    conn = sqlite3.connect('bank.db') 
    c = conn.cursor()
    c.execute("INSERT INTO Users VALUES (:fname, :lname, :bank, :user_id," 
     + ":salt, :key, :svg_acct_id, :check_acct_id, :flag)",
        {'fname': fname, 'lname': lname, 'bank': bank, 'user_id': user_id,
        'salt': salt, 'key': key, 'svg_acct_id': svg_acct_id,
        'check_acct_id': check_acct_id, 'flag': 'a'})
    conn.commit()
    conn.close()

# insert account to table "Accounts"
def insert_account(acct_id, user_id, holder, bank, acct_type, balance):
    conn = sqlite3.connect('bank.db') 
    c = conn.cursor()
    c.execute("INSERT INTO Accounts VALUES (:acct_id, :user_id, :holder, :bank, :acct_type, :balance)",
        {'acct_id': acct_id, 'user_id': user_id, 'holder': holder, 'bank': bank,
        'acct_type': acct_type, 'balance': balance})
    conn.commit()
    conn.close()

def insert_transaction(acct_id, user_id, trs_type, trs_to_or_from, trs_notes, amount, date):
    conn = sqlite3.connect('bank.db') 
    c = conn.cursor()
    c.execute("INSERT INTO Transactions VALUES (:acct_id, :user_id, :trs_type, :trs_to_or_from, :trs_notes, :amount, :date)",
                  {'acct_id': acct_id, 'user_id': user_id,
                   'trs_type': trs_type, 'trs_to_or_from': trs_to_or_from,
                   'trs_notes': trs_notes, 'amount': "+" + amount, 'date': date})
    conn.commit()
    conn.close()

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


create_table_users()
create_table_accounts()
create_table_transactions()
# delete_tables()
print_tables()

def validate_val(val):
    if val.isdigit():
        decimal_str = val + ".00"
        return decimal_str
    elif val[-3] == "." and val[:-3].isdigit() and val[-2:].isdigit():
        return val
    else:
        return "Invalid entry"




