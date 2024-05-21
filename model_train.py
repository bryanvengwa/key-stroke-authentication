import sqlite3

class DBManager:
    def __init__(self):
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('training_data.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        
        # Ensure the table exists

    def create_table(self):
        """Create the table if it doesn't exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS thresholds (
                                id INTEGER PRIMARY KEY,
                                good_threshold REAL,
                                bad_threshold REAL)''')
        self.conn.commit()

    def insert_good_threshold(self, good_threshold):
        """Insert a new good threshold record into the table."""
        self.cursor.execute("INSERT INTO thresholds (good_threshold) VALUES (?)", (good_threshold,))
        self.conn.commit()

    def insert_bad_threshold(self, bad_threshold):
        """Insert a new bad threshold record into the table."""
        self.cursor.execute("INSERT INTO thresholds (bad_threshold) VALUES (?)", (bad_threshold,))
        self.conn.commit()

    def get_all_records(self):
        """Retrieve all records from the table."""
        self.cursor.execute("SELECT * FROM thresholds")
        return self.cursor.fetchall()

    def get_specific_records(self, condition):
        """Retrieve records based on a given condition."""
        self.cursor.execute(condition)
        return self.cursor.fetchall()
    
    def calculate_average_good_threshold(self):
        """Calculate and return the average of all good thresholds."""
        # Fetch all records
        records = self.get_all_records()
        
        # Extract good thresholds
        good_thresholds = [record[1] for record in records]
        
        # Calculate the average
        if len(good_thresholds) > 0:
            average = sum(good_thresholds) / len(good_thresholds)
            return average
        else:
            return None