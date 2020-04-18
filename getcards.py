import csv
import json
import random
import string
from pprint import pprint

import regex
import requests
from PyInquirer import ValidationError, Validator, prompt

from card import Card
from csvutils import CSVIO
from generators import Generator
from privacy import PrivacySession
from stripeapi import StripeSession


class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            '^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end


class EmailValidator(Validator):
    def validate(self, document):
        ok = "@" in document.text
        if not ok:
            raise ValidationError(
                message='Please enter a valid email',
                cursor_position=len(document.text))  # Move cursor to end


class NameValidator(Validator):
    def validate(self, document):
        ok = " " in document.text
        if not ok:
            raise ValidationError(
                message='Please enter a valid first and last name',
                cursor_position=len(document.text))  # Move cursor to end


usesaved = [
    {
        'type': 'confirm',
        'name': 'useSaved',
        'message': 'Do you have settings saved here?'
    },
    {
        'type': 'input',
        'name': 'loadFile',
        'message': 'Enter a filename to load settings from:',
        'when': lambda answers: answers['useSaved'] == True
    },
]

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
        'validate': EmailValidator,
        'when': lambda answers: answers['cardProvider'] == 'privacy'
    },
    {
        'type': 'password',
        'name': 'privacyPassword',
        'message': 'What is your Privacy password?',
        'when': lambda answers: answers['cardProvider'] == 'privacy'
    },
    {
        'type': 'confirm',
        'name': 'privacyUnused',
        'message': 'Would you like to get only unused privacy cards?',
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
        'name': 'stripeNewCards',
        'message': 'Would you like to create new Stripe cards, or just get the existing ones?',
        'choices': ['New', 'Preexisting'],
        'filter': lambda val: val.lower(),
        'when': lambda answers: answers['cardProvider'] == 'stripe'
    },
    {
        'type': 'input',
        'name': 'stripeValue',
        'message': 'How many Stripe cards would you like to create?',
        'when': lambda answers: answers['cardProvider'] == 'stripe'
    },
    {
        'type': 'input',
        'name': 'stripeCardholder',
        'message': 'Enter a cardholder id which you would like to create new cards under.',
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
        'type': 'input',
        'name': 'email',
        'message': 'Enter an email (or catchall with @catchall.com) to use for creating profiles.',
        'validate': EmailValidator
    },
    {
        'type': 'input',
        'name': 'emailPrefix',
        'message': 'Enter an email prefix for your catchall, otherwise leave blank and one will be generated randomly.',
        'when': lambda answers: answers['email'][0] == "@"
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
    },
    {
        'type': 'confirm',
        'name': 'nameJig',
        'message': 'Do you need name jigging?',
    },
    {
        'type': 'input',
        'name': 'firstNames',
        'message': 'Enter a comma separated list of first names to use for jigging.',
        'when': lambda answers: answers['nameJig'] == True
    },
    {
        'type': 'input',
        'name': 'lastNames',
        'message': 'Enter a comma separated list of last names to use for jigging.',
        'when': lambda answers: answers['nameJig'] == True
    },
    {
        'type': 'input',
        'name': 'firstLast',
        'message': 'Enter a first and last name, separated by space, for creating profiles.',
        'when': lambda answers: answers['nameJig'] == False,
        'validate': NameValidator
    },
    {
        'type': 'input',
        'name': 'addressLine1',
        'message': 'Enter line 1 of an address to use for creating profiles.',
    },
    {
        'type': 'input',
        'name': 'addressLine2',
        'message': 'Enter line 2 of an address to use for creating profiles. (Leave blank for none)',
    },
    {
        'type': 'input',
        'name': 'city',
        'message': 'Enter a city to use for profiles.',
    },
    {
        'type': 'input',
        'name': 'state',
        'message': 'Enter a state to use for profiles (Two letter code or full state name)',
    },
    {
        'type': 'input',
        'name': 'zipCode',
        'message': 'Enter a zip code to use for profiles.',
    },
    {
        'type': 'input',
        'name': 'phoneNumber',
        'message': 'Enter a phone number to use for profiles.',
        'validate': PhoneNumberValidator
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
    templates = ""
    with open("config.json", "r") as f:
        templates = json.load(f)
    savedanswers = prompt(usesaved)
    promptsettings = ''
    if (savedanswers['useSaved']):
        try:
            with open(savedanswers['loadFile'] + ".json", "r") as settings:
                promptsettings = json.load(settings)
                pprint(promptsettings)
        except Exception as e:
            print("Could not find the settings file.")
            exit()
    else:
        promptsettings = prompt(questions)
        print('You entered:')
        pprint(promptsettings)
        if (promptsettings['saveSettings']):
            try:
                with open(promptsettings['saveFile'] + ".json", "w") as f:
                    json.dump(promptsettings, f)
            except Exception as e:
                print(e)
                print(
                    "Could not save settings. Please try again. (This may be a file permissions issue.)")
                exit()

    cardsession = ""
    cardlist = []
    firstname = ""
    lastname = ""

    if (promptsettings['nameJig'] == True):
        firstname = promptsettings['firstNames'].split(',')
        lastname = promptsettings['lastNames'].split(',')
    else:
        firstname = promptsettings['firstLast'].split(' ')[0]
        lastname = promptsettings['firstLast'].split(' ')[1]

    generator = Generator(firstname, lastname, promptsettings['email'], promptsettings['phoneNumber'], promptsettings['addressLine1'], promptsettings['addressLine2'], promptsettings['city'], promptsettings['state'], promptsettings['zipCode'], promptsettings['emailPrefix'], promptsettings['nameJig'], promptsettings['phoneJig'], promptsettings['addressJig'])

    if (promptsettings['cardProvider'] == "privacy"):
        cardsession = PrivacySession(
            promptsettings['privacyEmail'], promptsettings['privacyPassword'])
        cards = cardsession.getCards()
        transactions = cardsession.getTransactions()
        if (promptsettings['privacyUnused'] == True):
            cardlist = cardsession.findNewCards(cards, transactions)
            print("Total cards found: " + str(len(cardlist)))
        else:
            cardlist = cards
            print("Total cards found: " + str(len(cardlist)))
    elif (promptsettings['cardProvider'] == "stripe"):
        cardsession = StripeSession(promptsettings['stripeToken'])
        if (promptsettings['stripeNewCards'] == "new"):
            print("Generating {0} cards with cardholder {1}".format(
                promptsettings['stripeValue'], promptsettings['stripeCardholder']))
            for i in range(promptsettings['stripeValue']):
                cardholder = promptsettings['stripeCardholder']
                cardid = cardsession.createCard(cardholder)
                cardlist.append(cardsession.getCardDetails(cardid))
    else:
        pprint("Using own cards")

    print("Cards received, now generating profiles...")
    csvexporter = CSVIO("", "cardfile.csv", templates, generator)
    if (promptsettings['export'] == "ezmode4chefs"):
        csvexporter.writeEZMode(cardlist)
