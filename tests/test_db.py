# test_db_with_setup_teardown.py
import pytest
from utils.csv_reader import read_csv
from pathlib import Path

CSV_FILE = Path(__file__).parent / "../data" / "employees.csv"
csv_data = read_csv(CSV_FILE)



@pytest.mark.db
def test_insert_employee(db_connection, employees_table):
    """Insert a new employee"""
    cursor = employees_table
    insert_query = "INSERT INTO employees (name, salary, age) VALUES (%s, %s, %s)"
    data = ("Test Employee", 50000, 30)
    cursor.execute(insert_query, data)
    db_connection.commit()

    # Verify insertion
    cursor.execute("SELECT * FROM employees WHERE name = %s", (data[0],))
    result = cursor.fetchone()
    assert result['name'] == "Test Employee"
    assert result['salary'] == 50000
    assert result['age'] == 30


#csv_data = [("Alice", 50000, 28),("Bob", 60000, 32),("Charlie", 55000, 30),]

@pytest.mark.parametrize("name,salary,age", csv_data)
@pytest.mark.db
def test_update_employee(db_connection, employees_table , name, salary, age):
    """Update employee salary from CSV"""
    cursor = employees_table
    # Insert employee first
    cursor.execute(
        "INSERT INTO employees (name, salary, age) VALUES (%s, %s, %s)",
        (name, salary, age)
    )
    db_connection.commit()

    # Update salary (for example, increase by 10000)
    new_salary = salary + 10000
    cursor.execute(
        "UPDATE employees SET salary = %s WHERE name = %s",
        (new_salary, name)
    )
    db_connection.commit()

    # Verify update
    cursor.execute(
        "SELECT salary FROM employees WHERE name = %s",
        (name,)
    )
    result = cursor.fetchone()
    assert result['salary'] == new_salary

@pytest.mark.db
@pytest.mark.skip
def test_delete_employee(db_connection, employees_table):
    """Delete employee record"""
    cursor = employees_table
    # Insert employee first
    cursor.execute("INSERT INTO employees (name, salary, age) VALUES (%s,%s,%s)", ("Test Employee", 50000, 30))
    db_connection.commit()

    # Delete the employee
    cursor.execute("DELETE FROM employees WHERE name = %s", ("Test Employee",))
    db_connection.commit()

    # Verify deletion
    cursor.execute("SELECT * FROM employees WHERE name = %s", ("Test Employee",))
    result = cursor.fetchone()
    assert result is None, "Employee record was  deleted"

