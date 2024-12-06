from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# SQL Server Connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=wit-register-server.database.windows.net;'
    'DATABASE=WIT-Register-DB;'
    'UID=useradmin;'
    'PWD=P@ssw0rd!!!!'
)
cursor = conn.cursor()

# Home Page with Form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        school = request.form['school']

        # Insert data into SQL Server
        cursor.execute(
            "INSERT INTO Students (Name, PhoneNumber, Email, School) VALUES (?, ?, ?, ?)",
            (name, phone, email, school)
        )
        conn.commit()
        return "Student information submitted successfully!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
