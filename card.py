class Card:
    id = ""
    number = ""
    cvv = ""
    expmonth = ""
    expyear = ""
    unused = False

    def __init__(self, id, number, cvv, expmonth, expyear, unused):
        self.id = id
        self.number = number
        self.cvv = cvv
        self.expmonth = expmonth
        self.expyear = expyear
        self.unused = unused
