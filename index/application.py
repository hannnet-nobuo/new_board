from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_session import Session
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

@app.route('/')
def defalut():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    if('username' in session):
        return render_template('index.html', username=session.get('username'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if('username' in session):
        session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = None
        try: 
            post_email = request.form['email']
            post_pass = request.form['pass']
            user = client.board.user.find_one({"email":post_email,"pass":post_pass})
        except:
            None
        if(user):
            session['username'] = user['name']
            return redirect(url_for('index'))
        else:
            error = 'メールアドレスかパスワードが違います'
    return render_template('login.html', error=error)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

