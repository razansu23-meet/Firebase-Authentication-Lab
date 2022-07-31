from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {

  "apiKey": "AIzaSyA2Lp4oqWtkPy7g--SsG5oadKlgMqmZ74w",

  "authDomain": "cs-summer.firebaseapp.com",

  "projectId": "cs-summer",

  "storageBucket": "cs-summer.appspot.com",

  "messagingSenderId": "252748538991",

  "appId": "1:252748538991:web:e5c8261c5869b166f1199a",

  "measurementId": "G-LRWHHLNS0L" ,
  "databaseURL" : "https://cs-summer-default-rtdb.europe-west1.firebasedatabase.app/"

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('signin'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
            return render_template("signin.html")
    

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)