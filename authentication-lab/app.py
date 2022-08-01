from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyByNBMlAb6EljEkAVSXveD0fved4XDuu44",

  "authDomain": "labmeet-c935b.firebaseapp.com",

  "databaseURL": "https://labmeet-c935b-default-rtdb.europe-west1.firebasedatabase.app",

  "projectId": "labmeet-c935b",

  "storageBucket": "labmeet-c935b.appspot.com",

  "messagingSenderId": "827991363103",

  "appId": "1:827991363103:web:61b1333546351937078f2a",

  "measurementId": "G-8C0DDE2BH5"

}




firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        fullname = request.form['fullname']
        bio = request.form['bio']
        user={"email" : email , "username" : username , "password" : password , "fullname" : fullname}
        
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password )
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('signin'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    else:
        return render_template("signup.html")

    

@app.route('/signin', methods=['GET', 'POST'])
def signin():
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
    else:
        return render_template("signin.html")
    

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        try:
            title = request.form['title']
            text = request.form['text']
            tweet = {"title": title , "text":text , "uid":login_session['user']['localId']}
            db.child("Tweets").child(login_session['user']['localId']).push(user)
            return redirect(url_for('all_tweets'))
        except:
            error = "Authentication failed"
            return render_template("add_tweet.html")
    return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    
    a = db.child("Tweets").child(login_session['user']['localId']).get().val()
    return render_template("tweets.html" ,a=a )




if __name__ == '__main__':
    app.run(debug=True)