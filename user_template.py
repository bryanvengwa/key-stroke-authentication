import sqlite3
import numpy as np
import string
import random

class UserTemplate:
    def __init__(self, db_name):
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
                               (user_id TEXT PRIMARY KEY, features TEXT)''')
        self.connection.commit()

    def store_user_feature(self, user_id, features):
        # Store user features into the database
        self.cursor.execute('''INSERT INTO user_features VALUES (?, ?)''', (user_id, str(features)))
        self.connection.commit()

    def generate_random_paragraph(self):
        # Generate a random paragraph for the user to type
        paragraph = ''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(50, 200)))
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


# Example usage:
