import sqlite3
import numpy as np
import string
import random
import time
from pynput.keyboard import Key, Listener
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import numpy as np
import statistics
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
        return sqlite3.connect(self.db_name)
    

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
    def store_keystroke_data(self, event_type, event_time):
        # Store keystroke data into the database
        self.connection = self.connect_to_database()  # Create a new connection
        self.cursor = self.connection.cursor()
        self.cursor.execute('''INSERT INTO user_features (user_id, event_type, event_time) 
                           VALUES (?, ?, ?)''', (self.user_id, event_type, event_time))
        self.connection.commit()
      

    def on_press(self, key, event_time):
        # Handler for key press events
        if key == Key.esc:  # Check if the Escape key is pressed
            return False  # Stop listener
        try:
            # Record the key press event time
            self.store_keystroke_data('press', event_time)
        except AttributeError:
            # Ignore special keys
            pass
        return None

    def on_release(self, key, event_time):
        # Handler for key release events
        if key == Key.esc:  # Check if the Escape key is released
            self.connection.close()
            return False  # Stop listener
        # Record the key release event time
        self.store_keystroke_data('release', event_time)
        return None

    def start_capture(self, user_id):
        # Start capturing keystrokes for the specified user
        self.user_id = user_id
        print(self.user_id +"this is the id set to the template")
        with Listener(on_press=lambda k: self.on_press(k, time.time()),
                      on_release=lambda k: self.on_release(k, time.time())) as listener:
            self.connect_to_database()
            listener.join()
            # connection.close()

    def retrieve_user_keystrokes(self, user_id):
        # Retrieve keystroke data for the specified user from the database
        connection = self.connect_to_database()
        cursor = connection.cursor()
        cursor.execute('''SELECT event_type, event_time FROM user_features WHERE user_id = ?''', (user_id,))
        keystrokes = cursor.fetchall()
        connection.close()
        return keystrokes
    
    def get_user_id(self, user_name):
        self.connection = self.connect_to_database()
        cursor = self.connection.cursor()
        cursor.execute('''SELECT user_id FROM user_features WHERE user_name = ?''', (user_name,))
        user_id = cursor.fetchone()
        self.connection.close()
        if user_id:
            return user_id[0]
        else:
            return None
        

    def format_button_presses(self, data):
        """
        Formats a list of button press data into a dictionary with separate lists for presses and releases.

        Args:
            data: A list of tuples containing button state and timestamp.

        Returns:
            A dictionary with two keys: 'presses' and 'releases', each containing a list of timestamps.
        """
        presses = []
        releases = []
        for action, timestamp in data:
          if action == "press":
            presses.append(timestamp)
          else:
            releases.append(timestamp)
        return {"presses": presses, "releases": releases}    
    
    def record_keystrokes(self,):

        # Initialize the keystroke dictionary
        keystrokes = {'presses': [], 'releases': []}

        # Define the key press and release event handlers
        def on_press(key, event_time):
            if key == Key.esc:
                return False
            keystrokes['presses'].append(event_time)
            return None

        def on_release(key, event_time):
            if key == Key.esc:
                return False
            keystrokes['releases'].append(event_time)
            return None

        # Start capturing keystrokes for the specified user
        with Listener(on_press=lambda k: on_press(k, time.time()),
                      on_release=lambda k: on_release(k, time.time())) as listener:
            listener.join()

        return keystrokes
    def calculate_similarity(self, dict1, dict2, threshold=0.1):
        necessary_keys = {'presses', 'releases'}
    
        # Iterate over each necessary key
        for key in necessary_keys:
            # Check if the key exists in both dictionaries
            if key not in dict1 or key not in dict2:
                raise ValueError(f"One or both dictionaries do not contain the key '{key}'.")
            
        dict1_presses = [x for x in dict1['presses'] if x is not None]
        dict1_releases = [x for x in dict1['releases'] if x is not None]
        dict2_presses = [x for x in dict2['presses'] if x is not None]
        dict2_releases = [x for x in dict2['releases'] if x is not None]
            
        # Get minimum length of press and release data
        min_length_presses = min(len(dict1['presses']), len(dict2['presses']))
        min_length_releases = min(len(dict1['releases']), len(dict2['releases']))

        # Truncate longer lists to match shorter list length
        dict1['presses'] = dict1['presses'][:min_length_presses]
        dict1['releases'] = dict1['releases'][:min_length_releases]
        dict2['presses'] = dict2['presses'][:min_length_presses]
        dict2['releases'] = dict2['releases'][:min_length_releases]

          # Check for empty lists after filtering
        if len(dict1_presses) == 0 or len(dict1_releases) == 0:
            return None  # Indicate insufficient data for comparison
        
        # Calculate similarity scores using filtered lists
        press_similarities = []
        release_similarities = []
        for i in range(min(len(dict1_presses), len(dict2_presses))):
            press_similarities.append(abs(dict1_presses[i] - dict2_presses[i]))
        for i in range(min(len(dict1_releases), len(dict2_releases))):
            release_similarities.append(abs(dict1_releases[i] - dict2_releases[i]))
        
        # Use appropriate similarity metric (e.g., median absolute deviation)
        press_similarity = statistics.median(press_similarities)
        release_similarity = statistics.median(release_similarities)
        
        # Combine similarity scores (weighted average or other method)
        combined_similarity = (press_similarity + release_similarity) / 2
        
        return combined_similarity