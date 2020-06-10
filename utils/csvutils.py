import csv
from utils.generators import Generator
from utils.card import Card

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
            writer = csv.DictWriter(cardfile, fieldnames=self.templates['ezmode2'].keys(), delimiter='\t', lineterminator='\n')
            writer.writeheader()
            for card in cards:
                export = self.templates['ezmode2'].copy()
                export['BillingFirst'], export['BillingLast'] = self.generator.genName()
                export['CardName'] = export['BillingFirst'] + ' ' + export['BillingLast']
                export['BillingLine1'] = self.generator.genStreet()
                export['BillingLine2'] = self.generator.genAddress2()
                export['BillingCity'] = self.generator.city
                export['BillingState'] = self.generator.state
                export['BillingZip'] = self.generator.zip
                export['BillingCountry'] = "US"
                export['BillingPhone'] = self.generator.genPhone()
                export['ProfileName'] = card.cardid
                export['Email'] = self.generator.genEmail()
                export['CardNumber'] = card.number
                export['CardType'] = card.cardtype
                export['CardCVV'] = card.cvv
                export['CardMonth'] = card.expmonth
                export['CardYear'] = card.expyear
                writer.writerow(export)

    def readCSV(self):
        cardlist = []
        with open(self.infile, newline='') as cardfile:
            reader = csv.DictReader(cardfile)
            i = 0
            for row in reader:
                i+=1
                print(row)
                cardlist.append(Card("Card{}".format(i), row['CardType'], row['CardNumber'], row['CardCVV'], row['CardMonth'], row['CardYear'], True))
        return cardlist
