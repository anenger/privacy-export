import requests
import stripe
from card import Card

class StripeSession:

    def __init__(self, stripekey):
        stripe.api_key = stripekey

    def createCardholder(self):
        try:
            cardholder = stripe.issuing.Cardholder.create(
                name='Jenny Rosen',
                email='jenny.rosen@example.com',
                phone_number='+18008675309',
                status='active',
                type='individual',
                billing={
                    'address': {
                        'line1': '1234 Main Street',
                        'city': 'San Francisco',
                        'state': 'CA',
                        'postal_code': '94111',
                        'country': 'US',
                    },
                },
            )
            return cardholder.id
        except Exception as e:
            print(e)
            print("Could not create cardholder.")
            return

    def createCard(self, cardholder):
        try:
            card = stripe.issuing.Card.create(
                cardholder=cardholder,
                type='virtual',
                currency='usd',
            )
            return card.id
        except Exception as e:
            print(e)
            print("Could not create card.")
            return

    def getCardDetails(self, cardid):
        try:
            card = stripe.issuing.Card.details(cardid)
            unused = False
            if card.card.status == "active":
                unused = True
            else:
                unused = False
            return Card(card.card.id, card.number, card.cvc, card.exp_month, card.exp_year, unused)
        except Exception as e:
            print(e)
            print("Could not retrieve card.")
