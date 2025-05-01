import tkinter as tk
from tkinter import messagebox
from expenses import Expense
from income import Income

class ExpenseTrackerApp:
    def __init__(self, root, db):
        self.root = root
        self.root.title("FinWise - Expense & Income Tracker")
        self.db = db

        # Labels
        tk.Label(root, text="Amount:").grid(row=0, column=0)
        tk.Label(root, text="Category:").grid(row=1, column=0)
        tk.Label(root, text="Type:").grid(row=2, column=0)

        # Entry Fields
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1)

        # Dropdown for Type Selection
        self.type_var = tk.StringVar()
        self.type_var.set("Expense")
        self.type_menu = tk.OptionMenu(root, self.type_var, "Expense", "Income")
        self.type_menu.grid(row=2, column=1)

        # Buttons
        tk.Button(root, text="Add Transaction", command=self.add_transaction).grid(row=3, columnspan=2)
        tk.Button(root, text="Show Transactions", command=self.show_transactions).grid(row=4, columnspan=2)

    def add_transaction(self):
        """Handles adding a new transaction (expense/income)"""
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        transaction_type = self.type_var.get()

        if not amount or not category:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        amount = float(amount)

        if transaction_type == "Expense":
            transaction = Expense(amount, category)
        else:
            transaction = Income(amount, category)

        self.db.insert_transaction(transaction)
        messagebox.showinfo("Success", f"{transaction_type} added successfully!")

    def show_transactions(self):
        """Displays all transactions"""
        transactions = self.db.fetch_transactions()
        transaction_list = "\n".join([f"{t[1]} - {t[2]}: ${t[3]}" for t in transactions])
        messagebox.showinfo("Transaction History", transaction_list)
