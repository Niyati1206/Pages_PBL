from flask import Flask, request, redirect, url_for, flash, render_template, session
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = '9d7c1b02a57c3f74268a4f221ca5032a'

# Ensure that you have a folder to store uploads
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        full_name = request.form['full_name']
        dept = request.form['dept']
        email = request.form['email']
        password = request.form['password']


        # Hash the password before saving to database
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(''' 
                INSERT INTO users (full_name, email, dept, password) VALUES (?, ?, ?, ?)
            ''', (full_name, email, dept, hashed_password))
            conn.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("This email is already registered.", "error")
        finally:
            conn.close()

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form['email']
        password = request.form['password']

        # Hash the entered password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Query the database to check for the user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE email = ? AND password = ?''', (email, hashed_password))
        user = cursor.fetchone()

        if user:
            # User found, login successful
            session['user_id'] = user['id']  # Store user session
            session['user_email'] = user['email']  # Store email in session
            flash("Login successful!", "success")
            return redirect(url_for('upload_model_answer'))  # Redirect to dashboard (you can create this page)
        else:
            # Invalid credentials
            flash("Invalid email or password.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/upload_model_answer', methods=['GET', 'POST'])
def upload_model_answer():
    if request.method == 'POST':
        # Retrieve form data
        subject_name = request.form['subject-name']
        
        # Retrieve uploaded files
        section1 = request.files['section1']
        section2 = request.files['section2']
        section3 = request.files['section3']

        # Save the uploaded files in the 'uploads' folder
        section1_path = os.path.join(app.config['UPLOAD_FOLDER'], section1.filename)
        section2_path = os.path.join(app.config['UPLOAD_FOLDER'], section2.filename)
        section3_path = os.path.join(app.config['UPLOAD_FOLDER'], section3.filename)

        section1.save(section1_path)
        section2.save(section2_path)
        section3.save(section3_path)

        # Save file paths into the database (You can change this to save binary data if needed)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO model_answers (subject_name, section1, section2, section3)
                          VALUES (?, ?, ?, ?)''', (subject_name, section1_path, section2_path, section3_path))
        conn.commit()
        conn.close()

        return redirect(url_for('success'))

    return render_template('upload_model_answer.html')

@app.route('/success')
def success():
    return "Model Answer Uploaded Successfully!"


if __name__ == '__main__':
    app.run(debug=True)
