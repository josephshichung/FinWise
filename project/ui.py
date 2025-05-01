import tkinter as tk
from tkinter import messagebox
from expenses import Expense
from income import Income
import matplotlib.pyplot as plt
from collections import defaultdict

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
        tk.Button(root, text="Show Balance", command=self.show_balance).grid(row=5, columnspan=2)
        tk.Button(root, text="Visualize Pie Chart", command=self.show_pie_chart).grid(row=6, columnspan=2)
        tk.Button(root, text="Clear All", command=self.clear_transactions).grid(row=7, columnspan=2)

    def add_transaction(self):
        """Handles adding a new transaction (expense/income)"""
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        transaction_type = self.type_var.get()

        if not amount or not category:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        if transaction_type == "Expense":
            transaction = Expense(amount, category)
        else:
            transaction = Income(amount, category)

        self.db.insert_transaction(transaction)
        messagebox.showinfo("Success", f"{transaction_type} added successfully!")

    def show_transactions(self):
        """Displays all transactions"""
        transactions = self.db.fetch_transactions()
        if not transactions:
            messagebox.showinfo("No Transactions", "No transactions found.")
            return
        transaction_list = "\n".join([f"{t[1]} - {t[2]}: ${t[3]}" for t in transactions])
        messagebox.showinfo("Transaction History", transaction_list)

    def show_balance(self):
        """Calculate and display current balance"""
        transactions = self.db.fetch_transactions()
        total = sum(t[3] if t[1] == "Income" else -t[3] for t in transactions)
        messagebox.showinfo("Balance", f"Current Balance: ${total:.2f}")

    def show_pie_chart(self):
        """Draws a pie chart of expenses and income categories"""
        transactions = self.db.fetch_transactions()
        category_totals = defaultdict(float)

        for t in transactions:
            key = f"{t[1]}: {t[2]}"  # e.g. "Expense: Food"
            category_totals[key] += t[3]

        if not category_totals:
            messagebox.showinfo("No Data", "No transactions to visualize.")
            return

        labels = list(category_totals.keys())
        sizes = list(category_totals.values())

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Income and Expense Distribution")
        plt.axis('equal')
        plt.show()

    def clear_transactions(self):
        """Deletes all transactions from database (use with caution)"""
        confirm = messagebox.askyesno("Clear All", "Are you sure you want to delete all transactions?")
        if confirm:
            self.db.cursor.execute("DELETE FROM transactions")
            self.db.conn.commit()
            messagebox.showinfo("Success", "All transactions cleared.")
