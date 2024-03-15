import sqlite3
from pynput.keyboard import Key, Listener
import time
import numpy as np

class FeatureExtractor:
    def __init__(self):
        self.key_press_times = []
        self.key_release_times = []
        self.key_intervals = []

    def process_key_event(self, event_type, event_time):
        if event_type == 'press':
            self.key_press_times.append(event_time)
        elif event_type == 'release':
            self.key_release_times.append(event_time)

    def calculate_intervals(self):
        if len(self.key_press_times) >= 2:
            for i in range(1, len(self.key_press_times)):
                interval = self.key_press_times[i] - self.key_press_times[i-1]
                self.key_intervals.append(interval)

    def extract_features(self):
        self.calculate_intervals()
        features = {
            'keypress_times': self.key_press_times,
            'keyrelease_times': self.key_release_times,
            'key_intervals': self.key_intervals
        }
        return features

    def store_features_in_db(self, features):
        conn = sqlite3.connect('keystroke_features.db')
        c = conn.cursor()
        keypress_times = str(features['keypress_times'])
        keyrelease_times = str(features['keyrelease_times'])
        key_intervals = str(features['key_intervals'])
        c.execute("INSERT INTO keystroke_features (keypress_times, keyrelease_times, key_intervals) VALUES (?, ?, ?)",
                 (keypress_times, keyrelease_times, key_intervals))
        conn.commit()
        conn.close()

def on_press(key):
    try:
        print('Key {} pressed'.format(key))
        extractor.process_key_event('press', time.time())
    except AttributeError:
        pass

def on_release(key):
    if key == Key.esc:
        extractor.process_key_event('release', time.time())
        return False

def create_database_and_table():
    conn = sqlite3.connect('keystroke_features.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS keystroke_features
                 (id INTEGER PRIMARY KEY, keypress_times TEXT, keyrelease_times TEXT, key_intervals TEXT)''')
    conn.commit()
    conn.close()

create_database_and_table()

extractor = FeatureExtractor()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

extracted_features = extractor.extract_features()
extractor.store_features_in_db(extracted_features)





class UserTemplate:
    def __init__(self, user_id, features):
        self.user_id = user_id
        self.features = features

def calculate_similarity(features1, features2):
    # Calculate Euclidean distance between two feature vectors
    return np.linalg.norm(features1 - features2)

def authenticate_user(user_templates, input_features, threshold):
    # Compare input features to stored templates
    for template in user_templates:
        similarity = calculate_similarity(template.features, input_features)
        if similarity < threshold:
            return template.user_id
    # If no match found
    return None

# Example usage:
# Assume user_templates is a list of UserTemplate objects with stored features for each user
user_templates = [UserTemplate('user1', np.array([1, 2, 3])),
                  UserTemplate('user2', np.array([4, 5, 6])),
                  UserTemplate('user3', np.array([7, 8, 9]))]

# Assume input_features is the extracted features from the user attempting to authenticate
input_features = np.array([2, 3, 4])

# Set similarity threshold for authentication
threshold = 2.0

# Authenticate user based on input features
authenticated_user = authenticate_user(user_templates, input_features, threshold)

if authenticated_user:
    print("Authenticated as:", authenticated_user)
else:
    print("Authentication failed.")
