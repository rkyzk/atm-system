class UserPartialInfo:

    def __init__(self, fname, lname, bank, salt, key, svg_dp, check_dp):
        self.fname = fname
        self.lname = lname
        self.bank = bank
        self.salt = salt
        self.key = key
        self.svg_dp = svg_dp
        self.check_dp = check_dp
