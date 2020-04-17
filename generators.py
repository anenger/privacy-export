import random

class Generator:
    firstnames = []
    lastnames = []
    phone = ""
    address = ""

    def __init__(self, firstnames, lastnames, phone, address):
        self.firstnames = firstnames
        self.lastnames = lastnames
        self.phone = str(phone)
        self.address = address

    def jigStreet(self):
    	spaceindex = self.address.find(' ')
    	if (spaceindex >= 0):
    		number = address[:spaceindex]
    		street = address[spaceindex+1:]
    		charactergen = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
    		return str(number) + ' ' + charactergen +  ' ' + street

    def genName(self):
    	return random.choice(self.firstnames), random.choice(self.lastnames)

    def genPhone(self):
    	phone = str(self.phone)
    	area = phone[:3]
    	digits = random.randrange(1111111,9999999)
	       return str(area) + str(digits)
