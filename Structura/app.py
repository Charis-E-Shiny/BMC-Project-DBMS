from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='charis123',  # replace 'pw' with your actual password
    database='BMCbase'
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('homepage'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            session['user'] = user['name']
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/homepage')
def homepage():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('homepage.html', user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Store email in session and proceed to OTP
        session['reset_email'] = request.form['email']
        session['otp'] = '1234'  # Static OTP for now
        return redirect(url_for('verify_otp'))
    return render_template('forgot_password.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        if request.form['otp'] == session.get('otp'):
            return redirect(url_for('reset_password'))
        else:
            return render_template('verify_otp.html', error="Incorrect OTP.")
    return render_template('verify_otp.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            return render_template('reset_password.html', error="Passwords do not match.")

        hashed_pw = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password=%s WHERE email=%s",
                       (hashed_pw, session['reset_email']))
        db.commit()
        session.clear()
        return redirect(url_for('login'))

    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
