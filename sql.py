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
    c.execute("""SELECT fname, lname, bank, user_id, svg_acct_id,
        check_acct_id, flag FROM Users""")
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
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        with conn:
            c.execute("""DROP TABLE Users""")
            c.execute("""DROP TABLE Accounts""")
            c.execute("""DROP TABLE Transactions""")
    except Exception as e:
        print("There was an error with the system."
            "The tables weren't deleted.")
        print(e)
    finally:
        conn.close()

def get_user_id(code):
    """
    Get a list of existing user IDs of the bank of selection
    and return the next available ID for that bank.

    Argument:
    code -- bank code
    """
    if code == "a":
        sql = "SELECT user_id FROM users WHERE user_id LIKE '1%'"
    elif code == "b":
        sql = "SELECT user_id FROM users WHERE user_id LIKE '2%'"
    else:
        sql = "SELECT user_id FROM users WHERE user_id LIKE '3%'"
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute(sql)
    list = c.fetchall()
    conn.close()
    # return the highest number used among existing IDs added by 1.
    return max(list[0]) + 1

def get_acct_ids(code):
    """
    Get a list of savings and checking account IDs, 
    find the highest number for each of both account IDs, 
    and return the next available IDs (highest existing numbers + 1).

    Argument:
    code -- bank code 
    """
    if code == "a":
        #  Store the prefixes of savings and checking account IDs of North Bank.
        sql_var = ["'11%'", "'12%'"]
    elif code == "b":
        # Do the same for East Bank
        sql_var = ["'21%'", "'22%'"]
    else:
        # Do the same for South Bank
        sql_var = ["'31%'", "'32%'"]
    new_accts = []

    # In the first round of the for loop below, store the next available savings account ID
    # In the second round, store the next available checking account ID
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    for var in sql_var:
        sql = "SELECT acct_id FROM accounts WHERE acct_id LIKE " + var
        c.execute(sql)
        list = c.fetchall()
        new_accts.append(int((max(list))[0]) + 1)
    conn.close()
    return new_accts
    
def create_new_accounts(new_accts_info):
    try:
        conn = sqlite3.connect('bank.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute('Begin')
        # insert user information to table "Users"
        c.execute("INSERT INTO Users VALUES (:fname, :lname, :bank, :user_id, :salt, "
                    ":key, :svg_acct_id, :check_acct_id, :flag)",
                  {'fname': new_accts_info.fname, 'lname': new_accts_info.lname,
                   'bank': new_accts_info.bank, 'user_id': new_accts_info.user_id,
                   'salt': new_accts_info.salt, 'key': new_accts_info.key,
                   'svg_acct_id': new_accts_info.svg_acct_id,
                   'check_acct_id': new_accts_info.check_acct_id, 'flag': 'a'})
        # insert savings account into table "Accounts"
        c.execute("INSERT INTO Accounts VALUES (:acct_id, :user_id, :holder, :bank, :acct_type, :balance)",
                  {'acct_id': new_accts_info.svg_acct_id, 'user_id': new_accts_info.user_id,
                   'holder': new_accts_info.holder, 'bank': new_accts_info.bank,
                   'acct_type': "savings", 'balance': new_accts_info.svg_dp})
        # insert checking account into table "Accounts"
        c.execute("INSERT INTO Accounts VALUES (:acct_id, :user_id, :holder, :bank, :acct_type, :balance)",
                  {'acct_id': new_accts_info.check_acct_id, 'user_id': new_accts_info.user_id,
                   'holder': new_accts_info.holder, 'bank': new_accts_info.bank,
                   'acct_type': "checking", 'balance': new_accts_info.check_dp})
        # insert the record of initial deposit to savings account into table "Transactions"
        c.execute("INSERT INTO Transactions VALUES (:acct_id, :user_id, :trs_type, :trs_to_or_from,"
        " :trs_notes, :amt_with_sign, :date)",
        {'acct_id': new_accts_info.svg_acct_id, 'user_id': new_accts_info.user_id,
         'trs_type': "deposit", 'trs_to_or_from': "NA",
         'trs_notes': "initial deposit", 'amt_with_sign': "+" + new_accts_info.svg_dp,
         'date': new_accts_info.date})
        # insert the record of initial deposit to checking account into table "Transactions"
        c.execute("INSERT INTO Transactions VALUES (:acct_id, :user_id, :trs_type, :trs_to_or_from,"
                  " :trs_notes, :amt_with_sign, :date)",
                  {'acct_id': new_accts_info.check_acct_id, 'user_id': new_accts_info.user_id,
                   'trs_type': "deposit", 'trs_to_or_from': "NA",
                   'trs_notes': "initial deposit", 'amt_with_sign': "+" + new_accts_info.check_dp,
                   'date': new_accts_info.date})
        conn.commit()
        print("The data have been stored in the database.")
    except Exception as e:
        print("There was an error. The data hasn't been inserted. Please try again.")
        print(e)
        if conn:
            conn.rollback()
    finally:
        conn.close()

def get_user_info(user_id):
    """
    Get user Info of the given user ID
    """
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = " + str(user_id))
    user = c.fetchone()
    return user
    conn.close()

def deactivate(user_id):
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        # c.execute("UPDATE Users SET flag = 's' WHERE user_id = " 
        #    + str(user_id))
        print("UPDATE Users SET flag = 's' WHERE user_id = " + str(user_id))
        conn.commit()
        print("The card has been deactivated. Please call the number "
                "on the back of your card for assistance.")
    except Exception as e:
        if conn:
            conn.rollback()
        print("There was an error with the system.")
        print(e)
    finally:
        conn.close()

def activate(user_id):
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute('Begin')
        c.execute("UPDATE users SET flag = 'a' WHERE user_id = "
             + str(user_id))
        conn.commit()
        message = "The card has been activated."
        return message
    except Exception as e:
        conn.rollback()
        print("There was an error.  The user card couldn't be activated.")
        print(e)
    finally:
        conn.close()

def withdraw(amount, check_acct_id, user_id):
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("SELECT balance FROM accounts WHERE acct_id = " + str(check_acct_id))
        old_balance = c.fetchone()
        new_balance = (D(old_balance[0]) - D(amount))
        if new_balance < 0:
            print("Not sufficient amount of money in the account.")
        else:
            c.execute('Begin')
            c.execute("UPDATE accounts SET balance = " + str(new_balance)
                      + " WHERE acct_id = " + str(check_acct_id))
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO Transactions VALUES (:acct_id, :user_id,"
                      " :trs_type, :trs_to_or_from, :trs_notes, :amt_with_sign, :date)",
                  {'acct_id': check_acct_id, 'user_id': user_id, 'trs_type': "withdrawal",
                   'trs_to_or_from': "NA", 'trs_notes': "NA",
                   'amt_with_sign': "-" + str(amount), 'date': date})
            conn.commit()
            print(f"\n{amount} has been withdrawn from your checking account."
                  f"\nPlease take your money and card.")
    except Exception as e:
        print("There was an error.  Withdrawal is not possible at this time.  Please try again.")
        print(e)
        if conn:
            conn.rollback()
        exit()
    finally:
        conn.close()   

def deposit(amount, check_acct_id, user_id):
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("SELECT balance FROM accounts WHERE acct_id = " + str(check_acct_id))
        old_balance = c.fetchone()
        new_balance = D(old_balance[0]) + D(amount)
        c.execute('Begin')
        c.execute("UPDATE accounts SET balance = " + str(new_balance)
                  + " WHERE acct_id = " + str(check_acct_id))
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO Transactions VALUES (:acct_id, :user_id,"
                  " :trs_type, :trs_to_or_from, :trs_notes, :amt_with_sign, :date)",
                  {'acct_id': check_acct_id, 'user_id': user_id, 'trs_type': "deposit",
                   'trs_to_or_from': "NA", 'trs_notes': "NA",
                   'amt_with_sign': "+" + str(amount), 'date': date})
        conn.commit()
        print(f"{amount} was added to your checking account.")
    except Exception as e:
        print("There was an error.  Deposit is not possible at this time.  Please try again.")
        print(e)
        if conn:
            conn.rollback()
        exit()
    finally:
        conn.close()

def get_recip_info(recip_acct_num):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    # Get the recipient's name from accounts
    c.execute("SELECT user_id, holder FROM accounts WHERE acct_id = " + str(recip_acct_num))
    recip = c.fetchone()
    conn.close()
    return recip

activate(100001)
print_tables()
"""
sql_user_1 = "INSERT INTO Users VALUES (:fname, :lname, :bank, :user_id, :salt, :key, :svg_acct_id, :check_acct_id, :flag)"
sql_user_2 = "{'fname': fname, 'lname': lname, 'bank': bank, 'user_id': user_id, 'salt': salt, 'key': key, 'svg_acct_id': svg_acct_id, 'check_acct_id': check_acct_id, 'flag': 'a'}"

def insert_user(fname, lname, bank, user_id, salt, key, svg_acct_id, check_acct_id):
    global sql_insert_user
    conn = sqlite3.connect('bank.db') 
    c = conn.cursor()
    c.execute(sql_user_1, sql_user_2)
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
"""
# delete_tables()
# print_tables()
#create_table_users()
#create_table_accounts()
#create_table_transactions()