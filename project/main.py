import tkinter as tk
from ui import ExpenseTrackerApp
from database import Database
from expenses import Expense
from income import Income
import csv
import os

# Initialize database
db = Database("data/users.db")

# Load from CSV
def load_initial_data(db):
    # Use absolute path based on current file location
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "data", "initial_transactions.csv")
    print("Looking for CSV at:", file_path)

    if not os.path.exists(file_path):
        print("CSV file not found!")
        return

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                transaction_type = row["type"]
                category = row["category"]
                amount = float(row["amount"])

                if transaction_type == "Expense":
                    transaction = Expense(amount, category)
                else:
                    transaction = Income(amount, category)

                db.insert_transaction(transaction)
                print(f"Inserted: {transaction_type} - {category} - ${amount}")
            except Exception as e:
                print("Error processing row:", row, "Error:", e)

# Read data from file automatically
load_initial_data(db)

# GUI
root = tk.Tk()
root.geometry("500x300")
app = ExpenseTrackerApp(root, db)
root.mainloop()
