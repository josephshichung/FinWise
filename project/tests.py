import pytest
from expenses import Expense
from income import Income
from database import Database

@pytest.fixture
def test_db():
    """Creates a temporary in-memory database for testing."""
    return Database(":memory:")

def test_create_expense():
    """Ensure Expense object is initialized correctly."""
    e = Expense(25.0, "Food")
    assert e.amount == 25.0
    assert e.category == "Food"
    assert e.transaction_type == "Expense"

def test_create_income():
    """Ensure Income object is initialized correctly."""
    i = Income(150.0, "Freelance")
    assert i.amount == 150.0
    assert i.category == "Freelance"
    assert i.transaction_type == "Income"

def test_insert_and_fetch_transactions(test_db):
    """Check if both Expense and Income are stored and fetched properly."""
    e = Expense(20, "Books")
    i = Income(100, "Gift")
    test_db.insert_transaction(e)
    test_db.insert_transaction(i)

    result = test_db.fetch_transactions()
    assert len(result) == 2
    assert result[0][1] == "Expense"
    assert result[0][2] == "Books"
    assert result[1][1] == "Income"
    assert result[1][2] == "Gift"

def test_empty_database_fetch(test_db):
    """Fetching from an empty database should return an empty list."""
    result = test_db.fetch_transactions()
    assert result == []

def test_total_balance_calculation(test_db):
    """Validate net balance calculation from transactions."""
    e = Expense(40, "Snacks")
    i1 = Income(100, "Salary")
    i2 = Income(20, "Bonus")
    test_db.insert_transaction(e)
    test_db.insert_transaction(i1)
    test_db.insert_transaction(i2)

    all_tx = test_db.fetch_transactions()
    total = sum(tx[3] if tx[1] == "Income" else -tx[3] for tx in all_tx)
    assert total == 80  # 100 + 20 - 40

if __name__ == "__main__":
    import pytest
    pytest.main(["-v"])
