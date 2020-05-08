import requests
from utils.card import Card
from pprint import pprint

class PrivacySession:
    sessionid = ""
    token = ""
    cards = []
    transactions = []

    def __init__(self, username, password):
        self.sessionid = self.prelogin()
        self.token = self.login(self.sessionid, username, password)

    def prelogin(self):
    	headers = {
    		'Accept': 'application/json, text/plain, */*',
    		'Accept-Encoding': 'gzip, deflate, br',
    		'Accept-Language': 'en-US,en;q=0.9',
    		'Connection': 'keep-alive',
    		'Content-Type': 'application/json;charset=UTF-8',
    		'Host': 'privacy.com',
    		'Origin': 'https://privacy.com',
    		'Referer': 'https://privacy.com/login',
    		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    	}
    	print("Starting pre-login...")
    	r = requests.get('https://privacy.com/login', headers=headers)
    	print("Got pre-login response")
    	if (r.status_code == 200):
    		try:
    			print("Got sessionID header")
    			return r.headers['set-cookie'].split("; ")[0].replace('sessionID=', '')
    		except:
    			print("Error getting pre-login sessionID")
    	else:
    		print('Bad response when getting pre-login - ' + r.text)

    def login(self, sessionid, username, password):
    	cookies = {
    		'ETag':'"ps26i5unssI="',
    		'sessionID':sessionid
    	}
    	headers = {
    		'Origin': 'https://privacy.com',
    		'Accept-Encoding': 'gzip, deflate, br',
    		'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
    		'User-Agent': 'privacy-app/2.11.0.3 iOS/12.0',
    		'Content-Type': 'application/json;charset=UTF-8',
    		'Accept': 'application/json, text/plain, */*',
    		'Referer': 'https://privacy.com/login',
    		'Connection': 'keep-alive',
    		'DNT': '1',
    	}
    	data = {
    		'email':username,
    		'password':password
    	}
    	print("Starting login...")
    	r = requests.post('https://privacy.com/auth/local', headers=headers, cookies=cookies, json=data)
    	print("Got login response")
    	if (r.status_code == 200):
    		try:
    			body = r.json()
    			return body['token']
    		except Exception as e:
    			print("Error on login")
    			print(e)
    	else:
    		print(str(r.status_code) + ': Bad response when posting login form - ' + r.text)

    def getTransactions(self):
    	cookies = {
    		'sessionID':self.sessionid,
    		'token':self.token,
    		'ETag':'"ps26i5unssI="'
    	}
    	headers = {
    		'Accept': 'application/json, text/plain, */*',
    		'Accept-Encoding': 'gzip, deflate, br',
    		'Accept-Language': 'en-US,en;q=0.9',
    		'Authorization': 'Bearer ' + self.token,
    		'Cache-Control': 'no-cache',
    		'Connection': 'keep-alive',
    		'Content-Type': 'application/json;charset=UTF-8',
    		'DNT': '1',
    		'Host': 'privacy.com',
    		'Origin': 'https://privacy.com',
    		'Referer': 'https://privacy.com/home',
    		'User-Agent': 'privacy-app/2.11.0.3 iOS/12.0',
    	}
    	print('Getting transactions...')
    	r = requests.get('https://privacy.com/api/v1/transaction',cookies=cookies, headers=headers)
    	print('Got transaction response')
    	if (r.status_code == 200):
    		try:
    			return r.json()
    		except:
    			print("Error getting transactions")
    	else:
    		print('Bad response when getting transactions with code - ' + r.text)


    def findNewCards(self):
        cards = self.getCards()
        transactions = self.getTransactions()
        usedcardids = []
        newcards = []
        for transaction in transactions['transactionList']:
            if (transaction['cardID'] not in usedcardids):
                usedcardids.append(transaction['cardID'])
        for transaction in transactions['declineList']:
            if (transaction['cardID'] not in usedcardids):
                usedcardids.append(transaction['cardID'])
        for card in cards:
            if (int(card.cardid) not in usedcardids) or card.unused:
                newcards.append(card)
        return newcards


    def getCards(self):
    	cookies = {
    		'sessionID':self.sessionid,
    		'token':self.token,
    		'ETag':'"ps26i5unssI="'
    	}
    	headers = {
    		'Accept': 'application/json, text/plain, */*',
    		'Accept-Encoding': 'gzip, deflate, br',
    		'Accept-Language': 'en-US,en;q=0.9',
    		'Authorization': 'Bearer ' + self.token,
    		'Cache-Control': 'no-cache',
    		'Connection': 'keep-alive',
    		'Content-Type': 'application/json;charset=UTF-8',
    		'DNT': '1',
    		'Host': 'privacy.com',
    		'Origin': 'https://privacy.com',
    		'Referer': 'https://privacy.com/home',
    		'User-Agent': 'privacy-app/2.11.0.3 iOS/12.0',
    	}
    	print('Getting cards...')
    	r = requests.get('https://privacy.com/api/v1/card',cookies=cookies, headers=headers)
    	print('Got card response')
    	if (r.status_code == 200):
            try:
                cardlist = []
                for card in r.json()['cardList']:
                    if card['state'] == "OPEN":
                        cardlist.append(Card(card['cardID'], "Visa", card['PAN'], card['CVV'], card['expMonth'], card['expYear'], card['unused']))
                return cardlist
            except Exception as e:
                print(e)
                print("Error getting cards")
    	else:
    		print('Bad response when getting cards with code - ' + r.text)
