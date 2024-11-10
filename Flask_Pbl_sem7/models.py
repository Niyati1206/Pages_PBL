import sqlite3

# Initialize database and tables
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT UNIQUE,
        dept TEXT,
        password TEXT
    )''')

    # Model Answers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS model_answers (
        model_ans_id INTEGER PRIMARY KEY AUTOINCREMENT,
        section1 BLOB NOT NULL,
        section2 BLOB NOT NULL,
        section3 BLOB NOT NULL,
        subject_name TEXT
    )''')

    # Student Details Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_details (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT,
        student_name TEXT,
        marks_obtained INTEGER
    )''')

    conn.commit()
    conn.close()

# Call init_db when the script runs to create tables if they don't exist
init_db()
