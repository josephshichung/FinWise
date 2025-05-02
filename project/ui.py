import tkinter as tk
from tkinter import ttk, messagebox
from expenses import Expense
from income import Income
import matplotlib.pyplot as plt
from collections import defaultdict

class ExpenseTrackerApp:
    def __init__(self, root, db):
        self.root = root
        self.root.title("FinWise - Expense & Income Tracker")
        self.root.geometry("500x620")
        self.root.resizable(False, False)

        self.db = db
        self.build_layout()

    def build_layout(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#9E9E9E", font=("Helvetica", 10))
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Section Title
        ttk.Label(main_frame, text="Add Transaction", style="Header.TLabel").pack(pady=(0, 10))

        # Amount
        ttk.Label(main_frame, text="Amount:").pack(anchor="w")
        self.amount_entry = ttk.Entry(main_frame)
        self.amount_entry.pack(fill="x", pady=2)

        # Category
        ttk.Label(main_frame, text="Category:").pack(anchor="w")
        self.category_entry = ttk.Entry(main_frame)
        self.category_entry.pack(fill="x", pady=2)

        # Type
        ttk.Label(main_frame, text="Type:").pack(anchor="w")
        self.type_var = tk.StringVar(value="Expense")
        self.type_menu = ttk.OptionMenu(main_frame, self.type_var, "Expense", "Expense", "Income")
        self.type_menu.pack(fill="x", pady=2)

        # Buttons
        ttk.Button(main_frame, text="Add Transaction", command=self.add_transaction).pack(fill="x", pady=4)
        ttk.Button(main_frame, text="Show Transactions", command=self.show_transactions).pack(fill="x", pady=4)
        ttk.Button(main_frame, text="Show Balance", command=self.show_balance).pack(fill="x", pady=4)
        ttk.Button(main_frame, text="Visualize Pie Chart", command=self.show_pie_chart).pack(fill="x", pady=4)
        ttk.Button(main_frame, text="Clear All", command=self.clear_transactions).pack(fill="x", pady=4)

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)

        # Budget Goal Section
        ttk.Label(main_frame, text="Set Budget Goal", style="Header.TLabel").pack(pady=(0, 10))

        goal_frame = ttk.Frame(main_frame)
        goal_frame.pack(fill="x", pady=5)

        ttk.Label(goal_frame, text="Category:").grid(row=0, column=0, sticky="w")
        self.goal_category = ttk.Entry(goal_frame)
        self.goal_category.grid(row=1, column=0, padx=2, pady=2, sticky="ew")

        ttk.Label(goal_frame, text="Limit ($):").grid(row=0, column=1, sticky="w")
        self.goal_limit = ttk.Entry(goal_frame)
        self.goal_limit.grid(row=1, column=1, padx=2, pady=2, sticky="ew")

        goal_frame.columnconfigure(0, weight=1)
        goal_frame.columnconfigure(1, weight=1)

        ttk.Button(main_frame, text="Set Budget Goal", command=self.set_goal).pack(fill="x", pady=4)
        ttk.Button(main_frame, text="Check Budget Alerts", command=self.check_alerts).pack(fill="x", pady=4)

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

        plt.figure(figsize=(5,5))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,textprops={'size':8})
        plt.title("Income and Expense Distribution", fontweight= 'bold', loc='center')
        plt.axis('equal')
        plt.tight_layout()
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
