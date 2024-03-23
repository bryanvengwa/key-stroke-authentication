import sqlite3
from pynput.keyboard import Key, Listener
import time
import numpy as np

class FeatureExtractor:
    def __init__(self, db_name):
        self.db_name = db_name
        self.user_id = None
        self.keystrokes = []

    def connect_to_database(self):
        # Connect to the SQLite database
        return sqlite3.connect(self.db_name)

    def create_table(self, connection):
        # Create a table to store keystroke data if it doesn't exist
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS keystrokes
                          (user_id TEXT, event_type TEXT, event_time REAL)''')
        connection.commit()

    def store_keystroke_data(self, connection, event_type, event_time):
        # Store keystroke data into the database
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO keystrokes VALUES (?, ?, ?)''', (self.user_id, event_type, event_time))
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
        self.create_table(connection)
        with Listener(on_press=lambda k: self.on_press(connection, time.time()),
                      on_release=lambda k: self.on_release(connection, time.time())) as listener:
            listener.join()
        connection.close()

    def retrieve_user_keystrokes(self, user_id):
        # Retrieve keystroke data for the specified user from the database
        connection = self.connect_to_database()
        cursor = connection.cursor()
        cursor.execute('''SELECT event_type, event_time FROM keystrokes WHERE user_id = ?''', (user_id,))
        keystrokes = cursor.fetchall()
        connection.close()
        return keystrokes

# Example usage:
if __name__ == '__main__':
    # Create a FeatureExtractor instance
    extractor = FeatureExtractor('keystrokes.db')

    # Start capturing keystrokes for a specific user
    user_id = 'user1'
    extractor.start_capture(user_id)

    # Wait for a few seconds to capture keystrokes (replace this with your logic)
    time.sleep(5)

    # Stop capturing keystrokes

    # Retrieve and print keystrokes for the user from the database
    retrieved_keystrokes = extractor.retrieve_user_keystrokes(user_id)
    print("Retrieved Keystrokes for User:", retrieved_keystrokes)
 