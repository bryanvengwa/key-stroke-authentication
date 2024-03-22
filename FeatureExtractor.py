import sqlite3
from pynput.keyboard import Key, Listener
import time
import numpy as np

class FeatureExtractor:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.user_id = None
        self.keystrokes = []

    def start_capture(self, user_id):
        # Connect to the SQLite database
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

        # Create a table to store keystroke data if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_features
                               (user_id TEXT, event_type TEXT, event_time REAL)''')
        self.connection.commit()

        # Start capturing keystrokes for the specified user
        self.user_id = user_id
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def store_keystroke_data(self, event_type, event_time):
        # Store keystroke data into the database
        self.cursor.execute('''INSERT INTO keystrokes VALUES (?, ?, ?)''', (self.user_id, event_type, event_time))
        self.connection.commit()

    def on_press(self, key):
        # Handler for key press events
        try:
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

    def close_connection(self):
        # Close the database connection
        if self.connection:
            self.connection.close()

# # Example usage:
# if __name__ == '__main__':
#     # Create a FeatureExtractor instance
#     extractor = FeatureExtractor('keystrokes.db')

#     # Start capturing keystrokes for a specific user
#     user_id = 'user1'
#     extractor.start_capture(user_id)

#     # Wait for a few seconds to capture keystrokes (replace this with your logic)
#     time.sleep(5)

#     # Stop capturing keystrokes

#     # Retrieve and print keystrokes for the user from the database
#     retrieved_keystrokes = extractor.retrieve_user_keystrokes(user_id)
#     print("Retrieved Keystrokes for User:", retrieved_keystrokes)

#     # Close the database connection
#     extractor.close_connection()
