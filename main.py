from pynput.keyboard import Key, Listener
from user_template import UserTemplate
import numpy as np


template = UserTemplate('user_features.db')
template.connect_to_database()
template.create_table()

def log_a_user():
    print('Please enter your username')
    


def register_user(): 
    new_id = template.generate_user_id()
    print('Please Enter your username')
    user_name = input()
    print('creating a user with username : ' + user_name )
    template.register_user(new_id, user_name)
    print("Now type the paragraph below")
    paragraph_2 = template.generate_paragraph()
    print(paragraph_2)

    template.start_capture(new_id)
    print('we are passing the id ' + new_id)


def validate_action(action):
    if action == 1:
        register_user()
    elif action == 2:
        log_a_user()


def query_action(redo: bool):
    valid_numbers = [1, 2, 3]
    if redo:
        print("Please enter a valid number")
    else:
        print("What do you want to do ?")
    print("1. Register a user")
    print("2. Log a user into the system")
    print("Enter the number of your option.......")
    response = ''
    try:
        response = int(input())
    except:
        query_action(True)

    if response not in valid_numbers:
        query_action(True)
    else:
        validate_action(response)

    return response


query_action(False)
