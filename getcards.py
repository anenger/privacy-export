import requests
import json
import csv
import random
import string
import regex
from pprint import pprint
from PyInquirer import prompt, Validator, ValidationError,

class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end

class EmailValidator(Validator):
    def validate(self, document):
        ok = document.text.contains("@")
        if not ok:
            raise ValidationError(
                message='Please enter a valid email',
                cursor_position=len(document.text))  # Move cursor to end

questions = [
	{
		'type': 'list',
		'name': 'cardProvider',
		'message': 'Export Privacy, Stripe or your own cards?',
		'choices': ['Privacy', 'Stripe', 'Own'],
		'filter': lambda val: val.lower()
	},
	{
		'type': 'input',
		'name': 'privacyEmail',
		'message': 'What is your Privacy email?',
		'validate': EmailValidator
		'when': lambda answers: answers['cardProvider'] == 'privacy'
	},
	{
		'type': 'password',
		'name': 'privacyPassword',
		'message': 'What is your Privacy password?',
		'when': lambda answers: answers['cardProvider'] == 'privacy'
	},
	{
		'type': 'input',
		'name': 'stripeToken',
		'message': 'What is your Stripe token?',
		'when': lambda answers: answers['cardProvider'] == 'stripe'
	},
	{
		'type': 'list',
		'name': 'export',
		'message': 'Which style would you like the cards exported in?',
		'choices': ['EzMode4Chefs', 'Phantom', 'Ghost'],
		'filter': lambda val: val.lower()
	},
    {
        'type': 'confirm',
        'name': 'emailJig',
        'message': 'Do you need email jigging?',
    },
	{
		'type': 'input',
		'name': 'emailPrefix',
		'message': 'Enter an email prefix for your catchall, otherwise leave blank and one will be generated randomly.',
		'when': lambda answers: answers['emailJig'] == True
	},
	{
	    'type': 'confirm',
	    'name': 'addressJig',
	    'message': 'Do you need address jigging?',
	},
	{
		'type': 'confirm',
		'name': 'phoneJig',
		'message': 'Do you need phone jigging?'
	}
	{
		'type': 'confirm',
		'name': 'nameJig',
		'message': 'Do you need name jigging?',
	},
	{
		'type': 'confirm',
		'name': 'saveSettings',
		'message': 'Would you like to save these settings for future use?',
	},
	{
		'type': 'input',
		'name': 'saveFile',
		'message': 'Enter a filename to save settings to:',
		'when': lambda answers: answers['saveSettings'] == True
	},
]

if __name__ == "__main__":
	try:
		with open("config.json") as configfile:
			jsonfile = json.load(configfile)
	except Exception as e:
		print(e)
		print("Did you forget to rename the files? Bozo move...")
		exit()

	answers = prompt(questions)
	print('You entered:')
	pprint(answers)
