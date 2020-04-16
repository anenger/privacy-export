from PyInquirer import prompt, print_json

questions = [
    {
        'type': "input",
        'name': "first_name",
        'message': "What's your first name?",
    }
]

answers = prompt(questions)
print(answers)  # use the answers as input for your app