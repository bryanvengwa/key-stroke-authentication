import sqlite3
import numpy as np

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
                               (user_id TEXT, features TEXT)''')
        self.connection.commit()

    def store_user_feature(self, user_id, features):
        # Store user features into the database
        self.cursor.execute('''INSERT INTO user_features VALUES (?, ?)''', (user_id, str(features)))
        self.connection.commit()

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

# Example usage:
if __name__ == '__main__':
    # Create a UserTemplate instance
    user_template = UserTemplate('user_features.db')

    # Connect to the database
    user_template.connect_to_database()

    # Create the table if it doesn't exist
    user_template.create_table()

    # Simulate user features and store them into the database
    user_id = 'user1'
    user_features = np.array([1, 2, 3])
    user_template.store_user_feature(user_id, user_features)

    # Retrieve user features from the database
    retrieved_features = user_template.extract_user_feature(user_id)
    print("Retrieved Features:", retrieved_features)

    # Calculate similarity between user features
    if retrieved_features is not None:
        similarity = user_template.calculate_similarity(user_features, retrieved_features)
        print("Similarity:", similarity)
    else:
        print("User features not found.")

    # Close the
