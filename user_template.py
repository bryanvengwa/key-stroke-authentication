import sqlite3
import numpy as np
import string
import random
from pynput.keyboard import Key, Listener
import time

class UserTemplate:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.user_id = None
        self.keystrokes = []

    def connect_to_database(self):
        # Connect to the SQLite database
        return sqlite3.connect(self.db_name)
        # self.cursor = self.connection.cursor()

    def create_table(self):
        # Create a table to store user features if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_features
                               (user_id TEXT PRIMARY KEY, user_name, features TEXT)''')
        self.connection.commit()

    def store_user_feature(self, user_id, features):
        # Store user features into the database
        self.cursor.execute('''INSERT INTO user_features VALUES (?, ?)''', (user_id, str(features)))
        self.connection.commit()

    def generate_paragraph(self):
        # Generate a random paragraph for the user to type
        paragraph = 'The quick brown fox jumped over the lazy dogs and there was nothing to do about it so the owner of the dogs ended up selling the lazy dogs and bougth a a new breed that is a goldberg which is believed to be a special breed'
        return paragraph

    def extract_user_feature(self, user_id):
        # Retrieve user features from the database
        self.cursor.execute('''SELECT features FROM user_features WHERE user_id = ?''', (user_id,))
        feature_str = self.cursor.fetchone()
        if feature_str:
            return np.fromstring(feature_str[0], sep=',')  # Convert string back to numpy array
        else:
            return None

    def calculate_similarity(self, features1, features2):
        # Calculate Euclidean distance between two feature vectors
        return np.linalg.norm(features1 - features2)

    def close_connection(self):
        # Close the database connection
        if self.connection:
            self.connection.close()

    def generate_user_id(self):
        # Generate a unique user ID from keystrokes (example: first 5 characters)
        return ''.join(random.choices(string.ascii_lowercase, k=5))
    
    def register_user(self, user_id, user_name):
        self.cursor.execute('''INSERT INTO user_features (user_id, user_name) 
                           VALUES (?, ?)''', (user_id, user_name))
        self.connection.commit()
    
    # #### keystroke--stuff starts here -------
    def start_capture(self, user_id):
        # Start capturing keystrokes for the specified user
        self.user_id = user_id
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
    
    def on_press(self, key):
        # Handler for key press events
        
        try:
                # Check if the pressed key is the Escape key
            if key == Key.esc:
                self.stop_capture()  # Stop capturing if Escape key is pressed
            else:
                    # Record the key press event time
                    self.store_keystroke_data('press', time.time())
        except AttributeError:
                # Ignore special keys
                pass

    def on_release(self, key):
        # Handler for key release events
        # Record the key release event time
        self.store_keystroke_data('release', time.time())

    def retrieve_user_keystrokes(self, user_id):
        # Retrieve keystroke data for the specified user from the database
        self.cursor.execute('''SELECT event_type, event_time FROM keystrokes WHERE user_id = ?''', (user_id,))
        keystrokes = self.cursor.fetchall()
        return keystrokes


    


# Example usage:
