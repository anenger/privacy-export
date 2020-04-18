import random
import string

us_state_abbrev = {
    'alabama': 'AL',
    'alaska': 'AK',
    'american samoa': 'AS',
    'arizona': 'AZ',
    'arkansas': 'AR',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'delaware': 'DE',
    'district of columbia': 'DC',
    'florida': 'FL',
    'georgia': 'GA',
    'guam': 'GU',
    'hawaii': 'HI',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'iowa': 'IA',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'maine': 'ME',
    'maryland': 'MD',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'mississippi': 'MS',
    'missouri': 'MO',
    'montana': 'MT',
    'nebraska': 'NE',
    'nevada': 'NV',
    'new hampshire': 'NH',
    'new jersey': 'NJ',
    'new mexico': 'NM',
    'new york': 'NY',
    'north carolina': 'NC',
    'north dakota': 'ND',
    'northern mariana islands': 'MP',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'puerto rico': 'PR',
    'rhode island': 'RI',
    'south carolina': 'SC',
    'south dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'utah': 'UT',
    'vermont': 'VT',
    'virgin islands': 'VI',
    'virginia': 'VA',
    'washington': 'WA',
    'west virginia': 'WV',
    'wisconsin': 'WI',
    'wyoming': 'WY'
}


class Generator:
    firstname = ""
    lastname = ""
    phone = ""
    addressline1 = ""
    addressline2 = ""
    city = ""
    state = ""
    zip = ""

    def __init__(self, firstname, lastname, email, phone, addressline1, addressline2, city, state, zip, prefix, jigPhone, jigAddress):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = str(phone)
        self.addressline1 = addressline1
        self.addressline2 = addressline2
        self.city = city
        self.state = self.translateState(state)
        self.zip = zip
        self.prefix = prefix
        self.jigPhone = jigPhone
        self.jigAddress = jigAddress


    def translateState(self, state):
        if (len(state) == 2):
            return state.upper()
        else:
            try:
                statecode = us_state_abbrev[state.lower()]
                return statecode
            except KeyError as e:
                print("Could not find state in dict.")
                return None

    def genEmail(self):
        if ((self.email[0] == "@") and (self.prefix != "")):
            return self.prefix + str(random.randrange(111,999)) + self.email
        elif ((self.email[0] == "@") and (self.prefix == "")):
            return self.genName() + str(random.randrange(111,999)) + self.email
        else:
            return self.email

    def genStreet(self):
        if (self.jigAddress):
            spaceindex = self.addressline1.find(' ')
            if (spaceindex >= 0):
                number = self.addressline1[:spaceindex]
                street = self.addressline1[spaceindex + 1:]
                charactergen = random.choice(
                    string.ascii_uppercase) + random.choice(string.ascii_uppercase)
                return str(number) + ' ' + charactergen + ' ' + street
        else:
            return self.addressline1

    def genName(self):
        return random.choice(self.firstname), random.choice(self.lastname)

    def genPhone(self):
        if (self.jigPhone):
            phone = str(self.phone)
            area = phone[:3]
            digits = random.randrange(1111111, 9999999)
            return str(area) + str(digits)
        else:
            return self.phone
