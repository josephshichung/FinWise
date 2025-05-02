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

        self.build_layout()

    def build_layout(self):
        row = 0

        # Input fields
        tk.Label(self.root, text="Amount:").grid(row=row, column=0, sticky="w")
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=row, column=1)
        row += 1

        tk.Label(self.root, text="Category:").grid(row=row, column=0, sticky="w")
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=row, column=1)
        row += 1

        tk.Label(self.root, text="Type:").grid(row=row, column=0, sticky="w")
        self.type_var = tk.StringVar()
        self.type_var.set("Expense")
        self.type_menu = tk.OptionMenu(self.root, self.type_var, "Expense", "Income")
        self.type_menu.grid(row=row, column=1)
        row += 1

        # Action buttons
        tk.Button(self.root, text="Add Transaction", command=self.add_transaction).grid(row=row, columnspan=2, pady=2)
        row += 1
        tk.Button(self.root, text="Show Transactions", command=self.show_transactions).grid(row=row, columnspan=2, pady=2)
        row += 1
        tk.Button(self.root, text="Show Balance", command=self.show_balance).grid(row=row, columnspan=2, pady=2)
        row += 1
        tk.Button(self.root, text="Visualize Pie Chart", command=self.show_pie_chart).grid(row=row, columnspan=2, pady=2)
        row += 1
        tk.Button(self.root, text="Clear All", command=self.clear_transactions).grid(row=row, columnspan=2, pady=2)
        row += 1

        # Budget goal section
        tk.Label(self.root, text="Set Goal (Category + Limit):").grid(row=row, columnspan=2, pady=(10, 0))
        row += 1
        self.goal_category = tk.Entry(self.root)
        self.goal_category.grid(row=row, column=0)
        self.goal_limit = tk.Entry(self.root)
        self.goal_limit.grid(row=row, column=1)
        row += 1
        tk.Button(self.root, text="Set Budget Goal", command=self.set_goal).grid(row=row, columnspan=2, pady=2)
        row += 1
        tk.Button(self.root, text="Check Budget Alerts", command=self.check_alerts).grid(row=row, columnspan=2, pady=2)

    def add_transaction(self):
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

        transaction = Expense(amount, category) if transaction_type == "Expense" else Income(amount, category)
        self.db.insert_transaction(transaction)
        messagebox.showinfo("Success", f"{transaction_type} added successfully!")

    def show_transactions(self):
        transactions = self.db.fetch_transactions()
        if not transactions:
            messagebox.showinfo("No Transactions", "No transactions found.")
            return
        transaction_list = "\n".join([f"{t[1]} - {t[2]}: ${t[3]}" for t in transactions])
        messagebox.showinfo("Transaction History", transaction_list)

    def show_balance(self):
        transactions = self.db.fetch_transactions()
        total = sum(t[3] if t[1] == "Income" else -t[3] for t in transactions)
        messagebox.showinfo("Balance", f"Current Balance: ${total:.2f}")

    def show_pie_chart(self):
        transactions = self.db.fetch_transactions()
        category_totals = defaultdict(float)

        for t in transactions:
            key = f"{t[1]}: {t[2]}"
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
        confirm = messagebox.askyesno("Clear All", "Are you sure you want to delete all transactions?")
        if confirm:
            self.db.cursor.execute("DELETE FROM transactions")
            self.db.conn.commit()
            messagebox.showinfo("Success", "All transactions cleared.")

    def set_goal(self):
        category = self.goal_category.get()
        limit = self.goal_limit.get()
        if not category or not limit:
            messagebox.showerror("Error", "Both fields are required!")
            return
        try:
            limit = float(limit)
            self.db.insert_goal(category, limit)
            messagebox.showinfo("Success", f"Goal set for {category}: ${limit} per month")
        except ValueError:
            messagebox.showerror("Error", "Limit must be a number")

    def check_alerts(self):
        expenses = self.db.get_total_expenses_by_category()
        goals = self.db.get_goals()
        alerts = []
        for category, limit in goals:
            spent = expenses.get(category, 0)
            if spent > limit:
                alerts.append(f"Over budget in {category}: ${spent} spent > ${limit} goal")
        if alerts:
            messagebox.showwarning("Budget Alerts", "\n".join(alerts))
        else:
            messagebox.showinfo("Budget Alerts", "All spending is within limits!")
