import sqlite3
import numpy as np

class FeatureExtractor:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect_to_database(self):
        # Connect to the SQLite database
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        # Create a table to store keystroke data if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS keystrokes
                               (user_id TEXT, event_type TEXT, event_time REAL)''')
        self.connection.commit()

    def insert_keystroke_data(self, user_id, event_type, event_time):
        # Insert keystroke data into the table
        self.cursor.execute('''INSERT INTO keystrokes VALUES (?, ?, ?)''', (user_id, event_type, event_time))
        self.connection.commit()

    def extract_features_from_database(self, user_id):
        # Extract relevant features from the database for a specific user
        self.cursor.execute('''SELECT event_time FROM keystrokes WHERE user_id = ?''', (user_id,))
        event_times = self.cursor.fetchall()
        event_times = [time[0] for time in event_times]  # Extract event times from the fetched data
        # Perform feature extraction from event times (example: calculate intervals)
        features = np.diff(event_times) if len(event_times) >= 2 else []
        return features

    def close_connection(self):
        # Close the database connection
        if self.connection:
            self.connection.close()

# Example usage:
if __name__ == '__main__':
    # Create a FeatureExtractor instance
    extractor = FeatureExtractor('keystrokes.db')

    # Connect to the database
    extractor.connect_to_database()

    # Create the table if it doesn't exist
    extractor.create_table()

    # Simulate keystroke data and insert it into the database
    user_id = 'user1'
    events = [('press', 0.0), ('release', 0.1), ('press', 0.2), ('release', 0.3)]
    for event_type, event_time in events:
        extractor.insert_keystroke_data(user_id, event_type, event_time)

    # Extract features for the user from the database
    extracted_features = extractor.extract_features_from_database(user_id)
    print("Extracted Features:", extracted_features)

    # Close the database connection
    extractor.close_connection()

