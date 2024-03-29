import sqlite3
import numpy as np
import string
import random
import time
from pynput.keyboard import Key, Listener


class UserTemplate:
    def __init__(self, db_name):
        self.user_id = None
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect_to_database(self):
        # Connect to the SQLite database
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        # Create a table to store user features if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_features
                               (user_id TEXT, user_name TEXT, event_type TEXT, event_time REAL)''')
        self.connection.commit()


    def generate_paragraph(self):
        # Generate a random paragraph for the user to type
        paragraph = 'The quick brown fox jumped over the lazy dogs and there was nothing to do about it so the owner of the dogs ended up selling the lazy dogs and bougth a a new breed that is a goldberg which is believed to be a special breed'
        return paragraph

    def generate_user_id(self):
        # Generate a unique user ID from user_features (example: first 5 characters)
        return ''.join(random.choices(string.ascii_lowercase, k=5))
    
    def register_user(self, user_id, user_name):
        # Insert a new user into the database
        self.cursor.execute('''INSERT INTO user_features (user_id, user_name) 
                           VALUES (?, ?)''', (user_id, user_name))
        self.connection.commit()


    # keystrokes stuff
    def store_keystroke_data(self, connection, event_type, event_time):
        # Store keystroke data into the database
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO user_features (user_id, event_type, event_time) 
                           VALUES (?, ?, ?)''', (self.user_id, event_type, event_time))
        connection.commit()

    def on_press(self, connection, event_time):
        # Handler for key press events
        try:
            # Record the key press event time
            self.store_keystroke_data(connection, 'press', event_time)
        except AttributeError:
            # Ignore special keys
            pass

    def on_release(self, connection, event_time):
        # Handler for key release events
        # Record the key release event time
        self.store_keystroke_data(connection, 'release', event_time)

    def start_capture(self, user_id):
        # Start capturing keystrokes for the specified user
        self.user_id = user_id
        connection = self.connect_to_database()
        with Listener(on_press=lambda k: self.on_press(connection, time.time()),
                      on_release=lambda k: self.on_release(connection, time.time())) as listener:
            listener.join()
        connection.close()

    def retrieve_user_keystrokes(self, user_id):
        # Retrieve keystroke data for the specified user from the database
        connection = self.connect_to_database()
        cursor = connection.cursor()
        cursor.execute('''SELECT event_type, event_time FROM user_features WHERE user_id = ?''', (user_id,))
        keystrokes = cursor.fetchall()
        connection.close()
        return keystrokes


    


# Example usage:
