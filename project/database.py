import os
import sqlite3

class Database:
    def __init__(self, db_name):
        """Initialize database connection and create table if not exists."""
        
        # Ensure the 'data' directory exists
        os.makedirs(os.path.dirname(db_name), exist_ok=True)

        try:
            # Establish a connection to the SQLite database
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()

            # Create the table if it doesn't exist
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, type TEXT, category TEXT, amount REAL)"
            )
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Error while connecting to the database: {e}")
            raise

    def insert_transaction(self, transaction):
        """Inserts a transaction into the database."""
        try:
            self.cursor.execute(
                "INSERT INTO transactions (type, category, amount) VALUES (?, ?, ?)",
                (transaction.transaction_type, transaction.category, transaction.amount),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting transaction: {e}")
            raise

    def fetch_transactions(self):
        """Fetches all transactions."""
        try:
            self.cursor.execute("SELECT * FROM transactions")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching transactions: {e}")
            raise

    def close(self):
        """Closes database connection."""
        if self.conn:
            self.conn.close()

