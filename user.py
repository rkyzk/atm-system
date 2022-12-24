class User:

    def __init__(self, fname, lname, bank, user_id, salt, key, svg_acct_id,
                 check_acct_id, flag):
        self.fname = fname
        self.lname = lname
        self.bank = bank
        self.user_id = user_id
        self.salt = salt
        self.key = key
        self.svg_acct_id = svg_acct_id
        self.check_acct_id = check_acct_id
        self.flag = flag
