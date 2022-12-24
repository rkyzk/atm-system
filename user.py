class User:

    def __init__(self, fname, lname, holder, bank, user_id, salt, key, svg_acct_id,
                 check_acct_id, svg_dp, check_dp, date):
        self.fname = fname
        self.lname = lname
        self.holder = holder
        self.bank = bank
        self.user_id = user_id
        self.salt = salt
        self.key = key
        self.svg_acct_id = svg_acct_id
        self.check_acct_id = check_acct_id
        self.svg_dp = svg_dp
        self.check_dp = check_dp
        self.date = date