import tkinter as tk
from tkinter import simpledialog
from ui import ExpenseTrackerApp
from database import Database

# Prompt for username
def get_username():
    temp_root = tk.Tk()
    temp_root.withdraw()  # Hide the main window
    username = simpledialog.askstring("Login", "Enter your username:")
    temp_root.destroy()
    if not username:
        raise Exception("Username is required to continue.")
    return username.strip().lower()

def load_initial_data(db):
    # Skip CSV load if there are already transactions in the database
    if db.fetch_transactions():
        print("Existing user data found. Skipping CSV load.")
        return

    # If the database is empty, no CSV will be loaded for new users
    print("New user. Starting with an empty transaction history.")

# ---- App entry point ----
if __name__ == "__main__":
    try:
        username = get_username()

        db = Database(base_dir="data/users", user_db_name=username)

        load_initial_data(db)

        root = tk.Tk()
        root.geometry("500x300")
        app = ExpenseTrackerApp(root, db)
        root.mainloop()

    except Exception as e:
        print(f"Application closed or error occurred: {e}")
