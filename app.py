from flask import Flask, render_template, request, redirect, url_for
import random
import requests
import json


app = Flask(__name__)

# Dummy user data (username, password, and OTP)
users = {
    "user1",
    "user2"
}



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
    otp = request.form['otp']

    if authenticate_otp(username, otp):
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', message='Invalid username, password, or OTP')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
