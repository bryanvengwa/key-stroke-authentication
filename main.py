from pynput.keyboard import Key, Listener
from user_template import UserTemplate
import numpy as np

# from FeatureExtractor import FeatureExtractor

# this is the oneTime overall connection to the userTemplate class
template = UserTemplate('user_features.db')
# features = FeatureExtractor('user_features.db')
template.connect_to_database()
template.create_table()

# Define a function to handle keystroke events
#


if __name__ == '__main__':
    user_id = template.generate_user_id()
    # user_name = input()
    template.register_user(user_id, 'bryanvengwa')
    print("Now type the paragraph below")
    paragraph = template.generate_paragraph()
    print(paragraph)
    template.start_capture(user_id)
    strokes = template.retrieve_user_keystrokes(user_id)
    print(strokes)
    # features.start_capture(user_id)


def register_user():
    new_id = template.generate_user_id()
    print('Please Enter your username')
    user_name = input()
    template.register_user(new_id, user_name)
    print("Now type the paragraph below")
    paragraph_2 = template.generate_paragraph()
    print(paragraph_2)
    template.start_capture(new_id)
    # features.start_capture(user_id)


#     pass

# print("script is running ")

def validate_action(action):
    if action == 1:
        pass


def query_action(redo: bool):
    valid_numbers = [1, 2, 3]
    if redo:
        print("Please enter a valid number")
    else:
        print("What do you want to do ?")
    print("1. Register a user")
    print("2. Log a user into the system")
    print("3. Sign in a user")
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
