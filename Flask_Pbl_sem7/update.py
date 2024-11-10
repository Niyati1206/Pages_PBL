import sqlite3

def add_columns_to_students_details():
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Add new columns to the students_details table
    cursor.execute("ALTER TABLE student_details ADD COLUMN sectionA_marks INTEGER;")
    cursor.execute("ALTER TABLE student_details ADD COLUMN sectionB_marks INTEGER;")
    cursor.execute("ALTER TABLE student_details ADD COLUMN sectionC_marks INTEGER;")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to add the columns
add_columns_to_students_details()
