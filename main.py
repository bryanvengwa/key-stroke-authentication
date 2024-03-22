from pynput.keyboard import Key, Listener
from user_template import UserTemplate
import numpy as np

# this is the oneTime overall connection to the userTemplate class
template = UserTemplate('user_features.db')
template.connect_to_database()
template.create_table()


# Define a function to handle keystroke events
# 


# Define a function to handle key release events
# def on_release(key):
#     # If the ESC key is pressed, stop the listener
#     if key == Key.esc:
#         return False

# # Create a listener to monitor keystrokes
# with Listener(on_press=on_press, on_release=on_release) as listener:
#     # Start listening for events
#     listener.join()


# if __name__ == '__main__':
#     # Create a UserTemplate instance
#     user_template = UserTemplate('user_features.db')

#     # Connect to the database
#     user_template.connect_to_database()

#     # Create the table if it doesn't exist
#     user_template.create_table()

#     # Sign up functionality: Register a user
#     user_id = user_template.generate_user_id()
#     print("Generated User ID:", user_id)

#     # Generate random paragraph for the user to type
#     paragraph = user_template.generate_paragraph()
#     print("Random Paragraph for User to Type:", paragraph)

#     # Simulate user features (random for demonstration)
#     user_features = np.random.rand(10)
#     print("Simulated User Features:", user_features)

#     # Store user features into the database
#     user_template.store_user_feature(user_id, user_features)
#     print("User features stored in the database.")

#     # Close the database connection
#     user_template.close_connection()
    

# if __name__ == '__main__':

def register_user():
    print('Please Enter your username')
    user_id = template.generate_user_id()
    user_name = input()
    template.register_user(user_id, user_name)
    print("Now type the paragraph below")
    paragraph = template.generate_paragraph()
    print(paragraph)

    pass

print("script is running ")

def validate_action(action):
    if action == 1:
        register_user()


def query_action(redo : bool ):
    valid_numbers = [1,2,3]
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
        response =int(input())
    except:
        query_action(True)

    if response not in valid_numbers:
        query_action(True)
    else:    
        validate_action(response)

    return response

query_action(False)

    
    

# def validate_input(input):
 
#     print(valid_numbers , "here is the array")
    
#     validate_input(response)
# query_action(True)