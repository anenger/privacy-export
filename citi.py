from urllib import parse
import json
import csv

cardtext = ""
templates = ""
with open("citi.txt", "r") as f:
    cardtext = f.read()
    f.close()

with open("utils/exports.json", "r") as f:
    templates = json.load(f)

def writeCards(cards):
    with open("citicards.csv", mode='w+') as cardfile:
        writer = csv.DictWriter(cardfile, templates['import'].keys(), lineterminator='\n')
        writer.writeheader()
        for card in cards:
            export = templates['import'].copy()
            export['Merchant'] = card['name']
            export['CardType'] = card['type']
            export['CardName'] = "Andrew Enger"
            export['CardNumber'] = card['number']
            export['CardCVV'] = card['cvv']
            export['CardMonth'] = card['expmonth']
            export['CardYear'] = '20' + card['expyear']
            export['LeftOnCard'] = card['leftoncard']
            writer.writerow(export)


cardsdict = dict(parse.parse_qsl(parse.urlsplit(cardtext).path))
cardlist = []

for i in range(1, int(cardsdict['End']) + 1):
    expmonth = cardsdict['Expiry{}'.format(i)].split("/")[0]
    expyear = cardsdict['Expiry{}'.format(i)].split("/")[1]
    cardlist.append({
        "name":cardsdict['MerchantName{}'.format(i)],
        "type": "MasterCard",
        "number": cardsdict['PAN{0}'.format(i)],
        "cvv": cardsdict['AVV{0}'.format(i)],
        "expmonth": expmonth,
        "expyear": expyear,
        "leftoncard": cardsdict['OpenToBuy{0}'.format(i)]
    })

writeCards(cardlist)
