class UserPartialInfo:

    def __init__(self, fname, lname, bank_code, salt, key, svg_dp, check_dp):
        self.fname = fname
        self.lname = lname
        self.bank_code = bank_code
        self.salt = salt
        self.key = key
        self.svg_dp = svg_dp
        self.check_dp = check_dp