from flask import Flask, render_template, request, redirect, url_for
import random
import requests
import json


app = Flask(__name__)

# Dummy user data (username, password, and OTP)
users = {
    "user1": {"password": "password1", "otp": "123456"},
    "user2": {"password": "password2", "otp": "654321"}
}

# Function to generate a random OTP
def get_otp():

    return str(random.randint(100000, 999999))

# Function to check if username and password are valid
def authenticate_user(username, password):
    if username in users and users[username]["password"] == password:
        return True
    return False

# Function to check if OTP is valid
def authenticate_otp(username, otp):
    url = "http://10.55.14.69/fs/otp.json"
    headers = {"Authorization": "Basic Og=="}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        otp_code = json_data.get("OTP")
        if otp_code:
            print("OTP code:", otp_code)
        else:
            print("OTP code not found in JSON data.")
    else:
        print(f"Failed to fetch JSON data. Status code: {response.status_code}")


    if username in users and otp_code == otp:
        return True
    return False

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    otp = request.form['otp']

    if authenticate_user(username, password) and authenticate_otp(username, otp):
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', message='Invalid username, password, or OTP')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
