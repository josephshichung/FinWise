class Expense:
    def __init__(self, amount, category):
        """Expense object representing a financial expense."""
        self.amount = amount
        self.category = category
        self.transaction_type = "Expense"
