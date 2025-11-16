# Program Name: Assignment4.py
# Course: IT3883/Section W01
# Student Name: Ayomide Laosun
# Assignment Number: 3
# Due Date: 11/16/2025
# Purpose: This program reads temperature data from a text file, stores it in a SQLite database table, and then uses SQL queries to calculate and display the average temperature for Sunday and Thursday.
# Resources: Python documentation for sqlite3 module, Python documentation for file input and output

import csv
import sqlite3
import sys
import os

# Default SQLite database filename
DB_DEFAULT = "Assignment5.db"

# Target table name
TABLE = "readings"

# Map any capitalization to a clean day label
VALID_DAYS = {
    "sunday": "Sunday",
    "monday": "Monday",
    "tuesday": "Tuesday",
    "wednesday": "Wednesday",
    "thursday": "Thursday",
    "friday": "Friday",
    "saturday": "Saturday",
}

def normalize_day(name: str):
    """
    Convert any capitalization of a weekday into a consistent label.
    Returns None if the token is not a valid weekday.
    """
    if not name:
        return None
    return VALID_DAYS.get(str(name).strip().lower())

def init_db(conn: sqlite3.Connection):
    """
    Create the target table if it does not exist.
    """
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Day_Of_Week TEXT NOT NULL,
            Temperature_Value REAL NOT NULL
        )
        """
    )
    conn.commit()

def clear_table(conn: sqlite3.Connection):
    """
    Remove any old rows so re-running the program produces clean results.
    """
    conn.execute(f"DELETE FROM {TABLE}")
    conn.commit()

def parse_rows(input_file: str):
    """
    Yield (day, temperature) tuples from the input file.

    Accepted formats per line:
      - CSV: Day,Temp
      - Space separated: Day Temp

    Ignores empty lines and a header row if present.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue  # skip blank lines

            day = None
            temp = None

            # Try CSV style first
            if "," in s:
                for row in csv.reader([s]):
                    if len(row) >= 2:
                        day = normalize_day(row[0])
                        try:
                            temp = float(row[1])
                        except Exception:
                            temp = None
            else:
                # Fallback to space separated
                parts = s.split()
                if len(parts) >= 2:
                    day = normalize_day(parts[0])
                    try:
                        temp = float(parts[1])
                    except Exception:
                        temp = None

            # Skip header-like or malformed rows
            if day is None or temp is None:
                continue

            yield day, temp

def load_into_db(conn: sqlite3.Connection, rows):
    """
    Insert parsed rows into the database.
    """
    conn.executemany(
        f"INSERT INTO {TABLE} (Day_Of_Week, Temperature_Value) VALUES (?, ?)",
        list(rows)
    )
    conn.commit()

def avg_for(conn: sqlite3.Connection, day_name: str):
    """
    Return the average temperature for a given day, or None if no rows exist.
    """
    cur = conn.execute(
        f"SELECT AVG(Temperature_Value) FROM {TABLE} WHERE Day_Of_Week = ?",
        (day_name,)
    )
    row = cur.fetchone()
    return row[0] if row and row[0] is not None else None

def count_rows(conn: sqlite3.Connection) -> int:
    """
    Count how many rows are in the table.
    """
    cur = conn.execute(f"SELECT COUNT(*) FROM {TABLE}")
    return cur.fetchone()[0]

def format_avg(value):
    """
    Format average for printing.
    """
    return "N/A" if value is None else f"{value:.2f}"

def main():
    """
    CLI usage:
      python Assignment5.py input.txt [output.db]

    If no arguments are provided:
      input file defaults to 'Assignment5input.txt' in current directory.
      database defaults to 'Assignment5.db' in current directory.
    """
    input_file = sys.argv[1] if len(sys.argv) > 1 else "Assignment5input.txt"
    db_file = sys.argv[2] if len(sys.argv) > 2 else DB_DEFAULT

    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        sys.exit(1)

    # Connect to SQLite and ensure schema
    conn = sqlite3.connect(db_file)
    try:
        init_db(conn)
        clear_table(conn)

        # Parse file and insert rows
        rows = list(parse_rows(input_file))
        load_into_db(conn, rows)

        # Required averages via SQL
        sunday_avg = avg_for(conn, "Sunday")
        thursday_avg = avg_for(conn, "Thursday")

        # Print output to console
        print(f"Rows inserted: {count_rows(conn)}")
        print(f"Average Sunday temperature: {format_avg(sunday_avg)}")
        print(f"Average Thursday temperature: {format_avg(thursday_avg)}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()