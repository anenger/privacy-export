class Card:
    cardid = ""
    cardtype = ""
    number = ""
    cvv = ""
    expmonth = ""
    expyear = ""
    unused = False

    def __init__(self, cardid, cardtype, number, cvv, expmonth, expyear, unused):
        self.cardid = cardid
        self.cardtype = cardtype
        self.number = number
        self.cvv = cvv
        self.expmonth = expmonth
        self.expyear = expyear
        self.unused = unused
