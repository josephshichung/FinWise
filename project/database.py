import os
import sqlite3
from tkinter import messagebox

class Database:
    def __init__(self, db_name):
        os.makedirs(os.path.dirname(db_name), exist_ok=True)

        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, type TEXT, category TEXT, amount REAL)"
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    monthly_limit REAL
                )
                """
            )

            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Error while connecting to the database: {e}")
            raise

    def insert_transaction(self, transaction):
        try:
            self.cursor.execute(
                "INSERT INTO transactions (type, category, amount) VALUES (?, ?, ?)",
                (transaction.transaction_type, transaction.category, transaction.amount),
            )
            self.conn.commit()

            # Alert check only for Expense
            if transaction.transaction_type == "Expense":
                self.check_goal_alert(transaction.category)

        except sqlite3.Error as e:
            print(f"Error inserting transaction: {e}")
            raise

    def check_goal_alert(self, category):
        self.cursor.execute(
            "SELECT monthly_limit FROM goals WHERE LOWER(TRIM(category)) = LOWER(TRIM(?))",
            (category,)
        )
        result = self.cursor.fetchone()
        if result:
            limit = result[0]
            self.cursor.execute(
                "SELECT SUM(amount) FROM transactions WHERE type='Expense' AND LOWER(TRIM(category)) = LOWER(TRIM(?))",
                (category,)
            )
            total = self.cursor.fetchone()[0] or 0
            if total > limit:
                try:
                    messagebox.showwarning(
                        "Budget Alert",
                        f"Over budget in {category}:\nSpent ${total:.2f} > Goal ${limit:.2f}"
                    )
                except:
                    print(f"[WARNING] Over budget in {category}: Spent ${total:.2f} > Goal ${limit:.2f}")

    def fetch_transactions(self):
        try:
            self.cursor.execute("SELECT * FROM transactions")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching transactions: {e}")
            raise

    def insert_goal(self, category, limit):
        self.cursor.execute(
            "INSERT INTO goals (category, monthly_limit) VALUES (?, ?)",
            (category, limit)
        )
        self.conn.commit()

    def get_goals(self):
        self.cursor.execute("SELECT category, monthly_limit FROM goals")
        return self.cursor.fetchall()

    def get_total_expenses_by_category(self):
        self.cursor.execute(
            "SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category"
        )
        return dict(self.cursor.fetchall())

    def close(self):
        if self.conn:
            self.conn.close()
