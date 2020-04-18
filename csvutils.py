import csv
from generators import Generator
from card import Card

class CSVIO:
    infile = ""
    outfile = ""
    template = ""
    generator = ""

    def __init__(self, infile, outfile, templates, generator):
        self.infile = infile
        self.outfile = outfile
        self.templates = templates
        self.generator = generator

    def writeEZMode(self, cards):
        with open(self.outfile, mode='w') as cardfile:
            cardfile = csv.DictWriter(cardfile, self.templates['ezmode2'].keys(), lineterminator='\n')
            cardfile.writeheader()
            for card in cards:
                export = self.templates['ezmode2'].copy()
                export['BillingFirst'], export['BillingLast'] = self.generator.genName()
                export['CardName'] = export['BillingFirst'] + ' ' + export['BillingLast']
                export['BillingLine1'] = self.generator.genStreet()
                export['BillingLine2'] = self.generator.addressline2
                export['BillingCity'] = self.generator.city
                export['BillingState'] = self.generator.state
                export['BillingZip'] = self.generator.zip
                export['BillingCountry'] = "US"
                export['BillingPhone'] = self.generator.genPhone()
                export['ProfileName'] = card.id
                export['Email'] = self.generator.genEmail()
                export['CardNumber'] = card.number
                export['CardType'] = "Visa"
                export['CardCVV'] = card.cvv
                export['CardMonth'] = card.expmonth
                export['CardYear'] = card.expyear
                cardfile.writerow(export)

    def readCSV(self):
        return
