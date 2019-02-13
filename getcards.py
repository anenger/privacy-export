import requests
import json
import csv
import random
import string
from pprint import pprint

with open("config.json") as configfile:
	config = json.load(configfile)
	phantom = config['phantom']
	config = config['config']

def prelogin():
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
	if (r.status_code == requests.codes.ok):
		try:
			print("Got sessionID header")
			return r.headers['set-cookie'].split("; ")[0].replace('sessionID=', '')
		except:
			print("Error getting pre-login sessionID")
	else:
		print('Bad response when getting pre-login - ' + r.text)
	
def login(sessionid):
	cookies = {
		'ETag':'"ps26i5unssI="',
		'sessionID':sessionid
	}
	headers = {
		'Origin': 'https://privacy.com',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
		'Content-Type': 'application/json;charset=UTF-8',
		'Accept': 'application/json, text/plain, */*',
		'Referer': 'https://privacy.com/login',
		'Connection': 'keep-alive',
		'DNT': '1',
	}
	data = {
		'email':config['username'],
		'password':config['password']
	}
	print("Starting login...")
	r = requests.post('https://privacy.com/auth/local', headers=headers, cookies=cookies, json=data)
	print("Got login response")
	if (r.status_code == 200):
		try:
			body = r.json()
			if 'oneTimeCode' in body:
				if (body['oneTimeCode'] == True):
					print(body)
					code = raw_input("Please enter the one time code sent to the specified email: ")
					userToken = body['userToken']
					codeLogin(sessionid, code, userToken)
			else:
				return body['token']
		except Exception as e:
			print("Error on login")
			print(e)
	else:
		print(str(r.status_code) + ': Bad response when posting login form - ' + r.text)

def codeLogin(sessionid, code, userToken):
	headers = {
		'Accept': '*/*',
		'Accept-Encoding': 'br, gzip, deflate',
		'Accept-Language': 'en-us',
		'Connection': 'keep-alive',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Host': 'privacy.com',
		'sessionid': sessionid,
		'User-Agent': 'privacy-app/2.11.0.3 iOS/12.0',
	}
	form = {
		'userToken': userToken,
		'code': code
	}
	r = requests.post('https://privacy.com/auth/local/code', headers=headers, params=form)
	if (r.status_code == requests.codes.ok):
		try:
			return r.json()['token']
		except:
			print("Error getting login token")
	else:
		print('Bad response when login with code - ' + r.text)

def getCards(token,sessionid):
	cookies = {
		'sessionID':sessionid,
		'token':token,
		'ETag':'"ps26i5unssI="'
	}
	headers = {
		'Accept': 'application/json, text/plain, */*',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'en-US,en;q=0.9',
		'Authorization': 'Bearer ' + token,
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive',
		'Content-Type': 'application/json;charset=UTF-8',
		'DNT': '1',
		'Host': 'privacy.com',
		'Origin': 'https://privacy.com',
		'Referer': 'https://privacy.com/home',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
	}
	print('Getting cards...')
	r = requests.get('https://privacy.com/api/v1/card',cookies=cookies, headers=headers)
	print('Got card response')
	if (r.status_code == requests.codes.ok):
		try:
			return r.json()
		except:
			print("Error getting cards")
	else:
		print('Bad response when getting cards with code - ' + r.text)

def jigStreet(street):
	spaceindex = street.find(' ')
	if (spaceindex >= 0):
		number = street[:spaceindex]
		street = street[spaceindex+1:]
		charactergen = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
		return str(number) + ' ' + charactergen +  ' ' + street

def genName():
	firstname = ['Roosevelt','Fred','Christian','Alden','Virgilio','Lyman','Irving','Sidney','Shelby','Lewis','Bernardo','Jeramy','Carlos','Tuan','Wayne','Andres','Devon','Tomas','Luther','Norbert','Judson','Gerard','Brenton','Patrick','Saul','Williams','Jim','Herschel','Jackie','Lane','Anibal','Emile','Dale','Miquel','Harley','Jerome','Javier','Conrad','Lino','Ariel','Wyatt','Oscar','Carol','Forrest','Major','Horacio','Ernie','Garrett','Jere','Morton','Teddy','Bud','Cary','Samual','Enrique','Armando','Jeramy','Lonny','Mitchell','Noah','Pierre','Nathan','Cristopher','Elroy','Kent','Gustavo','Hal','Quincy','Guy','Kris','Rod','Sanford','Brett','Jamaal','Jonah','Leon','Dana','Giovanni','Scott','Danny','Dominique','Clifford','Claudio','Sandy','Raphael','Carrol','Leigh','Mathew','Lucien','Hong','Jarvis','Brenton','Bertram','Gary','Johnathon','Kelvin','Austin','Harris','Sean','Jacques']
	lastname = ['Rison','Shireman','Outlaw','Launius','Dear','Creswell','Rasor','Tsui','Roos','Kisner','Slavens','Friedlander','Pages','Gloor','Gryder','Masone','Litteral','Belt','Remo','Mixer','Izaguirre','Fleeman','Grizzard','Shiver','Kimberly','Cale','Grimshaw','Worden','Solberg','Cousar','Heatley','Cornforth','Mata','Styer','Huntington','Ragsdale','Allums','Tarnowski','Blodgett','Sipe','Zamudio','Heppner','Ornellas','Justis','Cranford','Cosper','Altizer','John','Hy','Stannard','Gale','Vanriper','Clutts','Mcshane','Simonetti','Gorton','Flaherty','Jeppesen','Kottke','Clatterbuck','Bilger','Lanham','Moffit','Troester','Dimaio','Pawlik','Lazenby','Loth','Wix','Madison','Mee','Hames','Cratty','Mccook','Wroblewski','Rushin','Stainbrook','Rachel','Kesner','Hesser','Rundle','Delahoussaye','Norrell','Riese','Andre','Erdman','Studivant','Dark','Northam','Sheehy','Yazzie','Buss','Fabiani','Hargrave','Kondo','Leclair','Dipaolo','Knudson','Pillow','Gearing']
	return random.choice(firstname), random.choice(lastname)

def genPhone(phone):
	phone = str(phone)
	area = phone[:3]
	digits = random.randrange(111111,999999)
	return str(area) + str(digits)


def writePhantom(info, cards):
	with open('cardfile.csv', mode='w') as cardfile:
		cardfile = csv.DictWriter(cardfile, info.keys(), lineterminator='\n')
		cardfile.writeheader()
		for card in cards['cardList']:
			if card['state'] == 'OPEN':
				export = info.copy()
				if (config['jigname'] == True):
					export['First Name'], export['Last Name'] = genName()
				if (config['jigphone'] == True):
					export['Phone'] = genPhone(export['Phone'])
				if (config['jigaddress'] == True):
					export['Shipping Address'] = jigStreet(export['Shipping Address'])
					export['Billing Address'] = export['Shipping Address']
				export['Profile Name'] = card['memo']
				export['Card Number'] = card['PAN']
				export['Card Type'] = 'visa'
				export['CVV'] = card['CVV']
				export['Expiry Month'] = card['expMonth']
				export['Expiry Year'] = card['expYear']
				cardfile.writerow(export)
			


def main():
	sessionid = prelogin()
	print(sessionid)
	token = login(sessionid)
	print(token)
	cards = getCards(token,sessionid)
	if (cards != None):
		if (config['export'] == 'phantom'):
			writePhantom(phantom, cards)

main()



