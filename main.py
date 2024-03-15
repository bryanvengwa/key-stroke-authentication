from pynput.keyboard import Key, Listener
from user_template import UserTemplate
import numpy as np
# Define a function to handle keystroke events
def on_press(key):
    try:
        # Print the pressed key
        print('Key {} pressed'.format(key))
    except AttributeError:
        # Ignore special keys
        pass

# Define a function to handle key release events
def on_release(key):
    # If the ESC key is pressed, stop the listener
    if key == Key.esc:
        return False

# Create a listener to monitor keystrokes
with Listener(on_press=on_press, on_release=on_release) as listener:
    # Start listening for events
    listener.join()


if __name__ == '__main__':
    # Create a UserTemplate instance
    user_template = UserTemplate('user_features.db')

    # Connect to the database
    user_template.connect_to_database()

    # Create the table if it doesn't exist
    user_template.create_table()

    # Sign up functionality: Register a user
    user_id = user_template.generate_user_id()
    print("Generated User ID:", user_id)

    # Generate random paragraph for the user to type
    paragraph = user_template.generate_random_paragraph()
    print("Random Paragraph for User to Type:", paragraph)

    # Simulate user features (random for demonstration)
    user_features = np.random.rand(10)
    print("Simulated User Features:", user_features)

    # Store user features into the database
    user_template.store_user_feature(user_id, user_features)
    print("User features stored in the database.")

    # Close the database connection
    user_template.close_connection()
