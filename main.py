from pynput.keyboard import Key, Listener
from user_template import UserTemplate
import numpy as np
from utils import record_keystrokes


template = UserTemplate('user_features.db')
template.connect_to_database()
template.create_table()

dict1 = {'presses': [1715939347, 1715939347.1898181, 1715939347.349696], 'releases': [1715939347.262229, 1715939347.341713, 1715939347.4337258]}
dict2 = {'presses': [1715939347.134788, 1715939347.1898181, 1715939347.349696], 'releases': [1715939347.262229, 1715939347.341713, 1715939347.4337258]}


print(template.calculate_similarity({'presses': [  1716278320.208875, 1716278320.212899, 1716278320.219866, 1716278320.230765, 1716278320.239615, 1716278320.283852, 1716278320.392831, 1716278320.460716, 1716278320.5887492, 1716278320.633779, 1716278320.648723, 1716278320.649406, 1716278320.7685602, 1716278320.795559, 1716278320.824834, 1716278320.920455, 1716278320.928077, 1716278321.008935, 1716278321.0847418, 1716278321.0924459, 1716278321.136597, 1716278321.1578062, 1716278321.3479838, 1716278321.364734, 1716278321.4856682], 'releases': [1716278320.058655, 1716278320.074975, 1716278320.078274, 1716278320.160864, 1716278320.204545, 1716278320.3116539, 1716278320.3290298, 1716278320.332475, 1716278320.384639, 1716278320.4162529, 1716278320.423595, 1716278320.560501, 1716278320.6414568,  1716278321.207423, 1716278321.3085592, 1716278321.400148, 1716278321.432537, 1716278321.476479, 1716278321.48461, 1716278321.520963]}, {'presses': [1716278319.8992882, 1716278319.906836, 1716278319.990597, 1716278320.100677, 1716278320.10489, 1716278320.208875, 1716278320.212899, 1716278320.219866, 1716278320.230765, 1716278320.239615, 1716278320.283852, 1716278320.392831, 1716278320.460716, 1716278320.5887492, 1716278320.633779, 1716278320.648723, 1716278320.649406, 1716278320.7685602, 1716278320.795559, 1716278320.824834, 1716278320.920455, 1716278320.928077, 1716278321.008935, 1716278321.0847418,  1716278321.364734, 1716278321.4856682], 'releases': [1716278320.058655, 1716278320.074975, 1716278320.078274, 1716278320.160864, 1716278320.204545, 1716278320.3116539, 1716278320.3290298, 1716278320.332475, 1716278320.384639, 1716278320.4162529, 1716278320.423595, 1716278320.560501, 1716278320.6414568, 1716278320.6937752, 1716278320.69412, ]}))

def log_a_user():
    print('Please enter your username')
    user_name = input()
    # get the user id for the user
    id = template.get_user_id(user_name )
    if id is None:
        print('You are not yet registered')
        print('You have to register first')
    else:
        print('Welcome ' + user_name )
        print('Type in the paragraph below')
        print(template.generate_paragraph())
        logging_in_strokes =  template.record_keystrokes()
        user_strokes = template.retrieve_user_keystrokes(id)
        formatted_user_strokes = template.format_button_presses(user_strokes)
        print("logging in data :" ,  logging_in_strokes)
        print("dataBase strokes :", formatted_user_strokes)

        similarity = template.calculate_similarity(logging_in_strokes, formatted_user_strokes)
        if similarity:
            print("You are logged in : " + user_name)
        else:
            print('Invalid similarity of keystrokes please try again later')




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
    print("3. Train the authentication model")
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
