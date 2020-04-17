import csv
from generators import Generator
from card import Card

class CSVIO:
    infile = ""
    outfile = ""
    template = ""
    generator = ""

    def __init__(self, infile, outfile, template, generator):
        self.infile = infile
        self.outfile = outfile
        self.template = template
        self.generator = generator

        def writeEZMode(self, cards):
            with open(self.outfile, mode='w') as cardfile:
                cardfile = csv.DictWriter(cardfile, self.template.keys(), lineterminator='\n')
                cardfile.writeheader()
                for card in cards:
                    export = self.template.copy()
                    export['BillingFirst'], export['BillingLast'] = jigName()
                    export['CardName'] = export['BillingFirst'] + ' ' + export['BillingLast']
                    export['BillingPhone'] = genPhone(export['BillingPhone'])
                    export['BillingLine1'] = jigStreet(export['BillingLine1'])
                    export['ProfileName'] = card['memo']
                    export['Email'] = 
                    export['CardNumber'] = card.number
                    export['CardType'] = card.type
                    export['CardCVV'] = card.cvv
                    export['CardMonth'] = card.exp_month
                    export['CardYear'] = card.exp_year
                    cardfile.writerow(export)

    def readCSV(self,):
        return
