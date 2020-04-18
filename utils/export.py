import csv

class Export:
    filepath = ""
    cards = {}

    def __init__(self, filepath, cards):
        self.filepath = filepath
        self.cards = cards


    def writeGhost(info, cards):
    	with open('cardfile.csv', mode='w') as cardfile:
    		cardfile = csv.DictWriter(cardfile, info.keys(), lineterminator='\n')
    		cardfile.writeheader()
    		for card in cards['cardList']:
    			if card['state'] == 'OPEN':
    				export = info.copy()
    				if (config['jigname']):
    					export['First Name'], export['Last Name'] = jigName()
    				if (config['jigphone']):
    					export['Phone'] = genPhone(export['Phone'])
    				if (config['jigaddress']):
    					export['Shipping Address'] = jigStreet(export['Shipping Address'])
    					export['Billing Address'] = export['Shipping Address']
    				export['Profile Name'] = card['memo']
    				export['Card Number'] = card['PAN']
    				export['Card Type'] = 'visa'
    				export['CVV'] = card['CVV']
    				export['Expiry Month'] = card['expMonth']
    				export['Expiry Year'] = card['expYear']
    				cardfile.writerow(export)

    def writeEzMode2(info, cards):
    	with open('cardfile.csv', mode='w') as cardfile:
    		cardfile = csv.DictWriter(cardfile, info.keys(), lineterminator='\n')
    		cardfile.writeheader()
    		for card in cards['cardList']:
    			if card['state'] == 'OPEN':
    				export = info.copy()
    				if (config['jigname']):
    					export['BillingFirst'], export['BillingLast'] = jigName()
    					export['CardName'] = export['BillingFirst'] + ' ' + export['BillingLast']
    				if (config['jigphone']):
    					export['BillingPhone'] = genPhone(export['BillingPhone'])
    				if (config['jigaddress']):
    					export['BillingLine1'] = jigStreet(export['BillingLine1'])
    				export['ProfileName'] = card['memo']
    				export['Email'] = prefix + str(random.randrange(111,999)) + '@' + export['Email']
    				export['CardNumber'] = card['PAN']
    				export['CardType'] = 'Visa'
    				export['CardCVV'] = card['CVV']
    				export['CardMonth'] = card['expMonth']
    				export['CardYear'] = card['expYear']
    				cardfile.writerow(export)
