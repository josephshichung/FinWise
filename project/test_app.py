import pytest
from expenses import Expense
from income import Income
from database import Database

@pytest.fixture
def test_db():
    """Creates a temporary in-memory database for testing."""
    return Database(":memory:")

def test_create_expense():
    e = Expense(25.0, "Food")
    assert e.amount == 25.0
    assert e.category == "Food"
    assert e.transaction_type == "Expense"

def test_create_income():
    i = Income(150.0, "Freelance")
    assert i.amount == 150.0
    assert i.category == "Freelance"
    assert i.transaction_type == "Income"

def test_insert_and_fetch_transactions(test_db):
    e = Expense(20, "Books")
    i = Income(100, "Gift")
    test_db.insert_transaction(e)
    test_db.insert_transaction(i)
    result = test_db.fetch_transactions()
    assert len(result) == 2
    assert result[0][1] == "Expense"
    assert result[1][1] == "Income"

def test_budget_goal_storage(test_db):
    test_db.insert_goal("Food", 200.0)
    goals = test_db.get_goals()
    assert len(goals) == 1
    assert goals[0][0] == "Food"
    assert goals[0][1] == 200.0

def test_budget_alert_trigger(monkeypatch, test_db):
    # Disable GUI warning during test
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *args, **kwargs: None)
    
    test_db.insert_goal("Snacks", 50)
    test_db.insert_transaction(Expense(60, "Snacks"))
    # If no exception was raised and no errors printed, success

def test_get_total_expenses_by_category(test_db):
    test_db.insert_transaction(Expense(10, "Transport"))
    test_db.insert_transaction(Expense(20, "Transport"))
    totals = test_db.get_total_expenses_by_category()
    assert totals["Transport"] == 30

def test_clear_transactions(test_db):
    test_db.insert_transaction(Expense(100, "Rent"))
    assert len(test_db.fetch_transactions()) == 1
    test_db.cursor.execute("DELETE FROM transactions")
    test_db.conn.commit()
    assert test_db.fetch_transactions() == []

def test_empty_database_fetch(test_db):
    assert test_db.fetch_transactions() == []

def test_total_balance_calculation(test_db):
    test_db.insert_transaction(Income(100, "Salary"))
    test_db.insert_transaction(Income(20, "Bonus"))
    test_db.insert_transaction(Expense(40, "Food"))
    txs = test_db.fetch_transactions()
    total = sum(t[3] if t[1] == "Income" else -t[3] for t in txs)
    assert total == 80

if __name__ == "__main__":
    import pytest
    pytest.main(["-v"])
