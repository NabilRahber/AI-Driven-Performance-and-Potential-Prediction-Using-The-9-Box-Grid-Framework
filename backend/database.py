"""
Database module — uses SQLite for storing uploaded employee datasets.
"""

import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "employee_data.db")


def get_connection():
    """Get a SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database — create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER NOT NULL,
            employee_name TEXT,
            data_json TEXT NOT NULL,
            FOREIGN KEY (dataset_id) REFERENCES datasets(id)
        )
    """)
    conn.commit()
    conn.close()


def store_dataset(filename: str, df: pd.DataFrame) -> int:
    """Store a dataset and its employee rows in the database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Insert the dataset record
    cursor.execute("INSERT INTO datasets (name) VALUES (?)", (filename,))
    dataset_id = cursor.lastrowid

    # Try to find a name column
    name_col = None
    for col in df.columns:
        if "name" in col.lower() or "employee" in col.lower():
            name_col = col
            break

    # Insert each employee row
    for _, row in df.iterrows():
        emp_name = str(row[name_col]) if name_col else f"Employee_{_}"
        data_json = row.to_json()
        cursor.execute(
            "INSERT INTO employees (dataset_id, employee_name, data_json) VALUES (?, ?, ?)",
            (dataset_id, emp_name, data_json),
        )

    conn.commit()
    conn.close()
    return dataset_id


def search_employees(query: str, dataset_id: int = None):
    """Search for employees by name."""
    conn = get_connection()
    cursor = conn.cursor()

    if dataset_id:
        cursor.execute(
            "SELECT id, dataset_id, employee_name, data_json FROM employees WHERE employee_name LIKE ? AND dataset_id = ? LIMIT 20",
            (f"%{query}%", dataset_id),
        )
    else:
        cursor.execute(
            "SELECT id, dataset_id, employee_name, data_json FROM employees WHERE employee_name LIKE ? ORDER BY id DESC LIMIT 20",
            (f"%{query}%",),
        )

    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_employee_by_id(employee_id: int):
    """Get a single employee by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, dataset_id, employee_name, data_json FROM employees WHERE id = ?",
        (employee_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_dataset_employees(dataset_id: int):
    """Get all employees for a dataset."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, dataset_id, employee_name, data_json FROM employees WHERE dataset_id = ?",
        (dataset_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_latest_dataset_id():
    """Get the latest dataset ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM datasets ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row["id"] if row else None
