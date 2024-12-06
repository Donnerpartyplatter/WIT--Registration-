from flask import Flask, render_template, request, flash, redirect, url_for
import pyodbc
import logging

app = Flask(__name__)

# Secret key for flash messaging
app.secret_key = 'your_secret_key'

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

# SQL Server Connection
try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=wit-register-server.database.windows.net;'
        'DATABASE=WIT-Register-DB;'
        'UID=useradmin;'
        'PWD=P@ssw0rd!!!!'
    )
    cursor = conn.cursor()
    logging.info("Successfully connected to the database.")
except pyodbc.Error as e:
    conn = None
    logging.error(f"Database connection failed: {e}")

# Home Page with Form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            school = request.form['school']

            if conn:
                # Insert data into SQL Server
                cursor.execute(
                    "INSERT INTO Students (Name, PhoneNumber, Email, School) VALUES (?, ?, ?, ?)",
                    (name, phone, email, school)
                )
                conn.commit()
                flash("Student information submitted successfully!", "success")
            else:
                flash("Database connection is unavailable. Please try again later.", "error")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
            flash("An error occurred while submitting your information. Please try again.", "error")
        return redirect(url_for('home'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
