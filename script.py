import mysql.connector as sqltor
import random
from getpass4 import getpass

pw = getpass("Enter MySql Password: \n")
mycon = sqltor.connect(host = 'localhost', user = 'root', password = pw, database = 'BMCbase')

if mycon.is_connected():
    print("Connection Successfull\n")
else:
    print("Error in mycon.isconnected()\n")


cur = mycon.cursor()

def generate_unique_userid():
    while True:
        userid = random.randint(1000, 9999)
        cur.execute("SELECT user_id from users WHERE user_id = %s", (userid,))
        result = cur.fetchone()
        if not result:
            return userid #Found Unique ID
        
def email_check():
    while True:
        email = input("Enter EmailID: \n")
        cur.execute("SELECT email from users WHERE email = %s", (email,))
        result = cur.fetchone()
        if not result:
            return email #valid email for signup
        else:
            print("Enter valid email\n")
            continue

def email_check_login():
    while True:
        email = input("Enter Email ID: \n")
        cur.execute("SELECT email FROM users WHERE email = %s", (email,))
        result = cur.fetchone()
        
        if result:
            return email  # Valid email for login
        else:
            print("Email not found. Redirecting to signup.\n")
            signup()
            break

def signup():
    userid = generate_unique_userid()
    name = input("Enter name: \n")
    email=email_check()
    snpassword = input("Enter Password: \n")
    role = input("Select Role(admin/business_owner/investor): \n")

    cur.execute("INSERT into users VALUES (%s, %s, %s, %s, %s)",(userid, name, email, snpassword, role)) 
    mycon.commit()

    print("Successful Signup\n")
    print("Directing to login\n")
    login()

def login():
    while True:
        email = email_check_login()
        cur.execute("SELECT password FROM users WHERE email = %s", (email,))
        result = cur.fetchone()

        if result:
            stored_password = result[0]
            password = getpass("Enter Password: \n")
            if password == stored_password:
                print("Login successful.")
                return email
            else:
                print("Incorrect password. Try again.\n")
        else:
            print("Email not found. Redirecting to signup.\n")
            signup()
            break

def forgotpassword():
    email = email_check_login()
    cur.execute("SELECT email FROM users WHERE email = %s", (email,))
    result = cur.fetchone()

    if result:
        new_password = input("Enter new password: \n")
        confirm_password = input("Confirm new password: \n")

        if new_password == confirm_password:
            cur.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
            mycon.commit()
            print("Password updated successfully.\n")
            print("redirecting to login\n")
            login()
        else:
            print("Passwords do not match. Try again.")
            forgotpassword()
    else:
        print("Email not found. Please sign up first.")
        signup()
