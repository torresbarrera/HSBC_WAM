

import pandas as pd
import sqlite3
import os

# --- Configuration ---
CSV_FILE = 'raw_workspace_data.csv'
DB_FILE = 'workspace_analytics.db'

# --- Schema Definition ---
# We will normalize the data into three tables:
# 1. spaces: Static information about each physical space.
# 2. employees: Static information about each employee.
# 3. bookings: Transactional data linking employees and spaces over time.

def create_database_schema(cursor):
    """Defines and creates the database tables."""
    # Drop tables if they exist to ensure a fresh start
    cursor.execute("DROP TABLE IF EXISTS bookings")
    cursor.execute("DROP TABLE IF EXISTS spaces")
    cursor.execute("DROP TABLE IF EXISTS employees")

    # Create spaces table
    cursor.execute("""
        CREATE TABLE spaces (
            Space_ID INTEGER PRIMARY KEY,
            Region TEXT,
            Country TEXT,
            City TEXT,
            Building TEXT,
            Floor INTEGER,
            Space_Type TEXT
        )
    """)

    # Create employees table
    cursor.execute("""
        CREATE TABLE employees (
            Employee_ID INTEGER PRIMARY KEY,
            Department TEXT
        )
    """)

    # Create bookings table
    cursor.execute("""
        CREATE TABLE bookings (
            Booking_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT,
            Time TEXT,
            Employee_ID INTEGER,
            Space_ID INTEGER,
            Activity_Type TEXT,
            Booking_Status TEXT,
            FOREIGN KEY (Employee_ID) REFERENCES employees (Employee_ID),
            FOREIGN KEY (Space_ID) REFERENCES spaces (Space_ID)
        )
    """)

def populate_database():
    """
    Reads the raw CSV data, normalizes it, and populates the
    SQLite database tables.
    """
    if not os.path.exists(CSV_FILE):
        print(f"Error: The file '{CSV_FILE}' was not found.")
        print("Please run 'generate_data.py' first.")
        return

    print(f"1. Reading data from '{CSV_FILE}'...")
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')


    # --- Normalize and Insert Data ---
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("2. Creating database schema...")
    create_database_schema(cursor)

    # Populate 'spaces' table
    print("3. Populating 'spaces' table...")
    spaces_df = df[['Space_ID', 'Region', 'Country', 'City', 'Building', 'Floor', 'Space_Type']].drop_duplicates()
    spaces_df.to_sql('spaces', conn, if_exists='append', index=False)

    # Populate 'employees' table
    print("4. Populating 'employees' table...")
    employees_df = df[['Employee_ID', 'Department']].drop_duplicates()
    employees_df.to_sql('employees', conn, if_exists='append', index=False)

    # Populate 'bookings' table
    print("5. Populating 'bookings' table...")
    bookings_df = df[['Date', 'Time', 'Employee_ID', 'Space_ID', 'Activity_Type', 'Booking_Status']]
    bookings_df.to_sql('bookings', conn, if_exists='append', index=False)

    # --- Verification ---
    print("6. Verifying inserted data...")
    for table_name in ['spaces', 'employees', 'bookings']:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"   - Found {count} records in '{table_name}'.")

    conn.commit()
    conn.close()

    print(f"\nSuccessfully created and populated '{DB_FILE}'.")
    print("Database ingestion complete.")


if __name__ == '__main__':
    populate_database()

