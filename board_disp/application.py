from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_session import Session
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)

app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

def not_login():
    if('username' not in session):
        return True
    return False

def redirect_no_login():
    return redirect(url_for('not_login_page'))

@app.route('/not_login_page')
def not_login_page():
    url = 'http://127.0.0.1:5000/index'
    return render_template('not_login_page.html', url=url)

@app.route('/')
def defalut():
    return redirect(url_for('index'))

@app.route('/index/<_id>', methods=['GET','POST'])
def index(_id):
    if(not_login()):
        return redirect_no_login()
    try:
        content = client.board.content.find_one({"_id":ObjectId(_id)})
    except:
        return "エラーです"
    if(content == None):
        return "掲示板が存在しません"
    users = client.board.user.find()
    disp_absences = []
    for user in users:
        temp_absence = {}
        temp_absence['user_id'] = user['_id']
        temp_absence['name'] = user['name']
        absence = client.board.absence.find_one({"user_id":user['_id'], "content_id":content['_id']})
        if (absence != None and absence['join'] == True):
            temp_absence['join'] = ' checked '
        disp_absences.append(temp_absence)

    return render_template('index.html',
                                    username=session.get('username'), 
                                    msg=content['msg'].replace('\n', '<br>').replace('\r', ''),
                                    title=content['title'],
                                    content_id=content['_id'],
                                    absences=disp_absences
                                    )

@app.route('/update/', methods=['POST'])
def update():
    json = request.get_json()
    if json['user_id'] == None or json['content_id'] == None:
        return 'エラーです'
    try:
        user_id = ObjectId(json['user_id'])
        content_id = ObjectId(json['content_id'])
        user = client.board.user.find_one({"_id":user_id})
        if(user == None):
            return 'ユーザが存在しません'
        content = client.board.content.find_one({"_id":content_id})
        if(content == None):
            return 'コンテンツが存在しません'

        one_absence = client.board.absence.find_one({"user_id":user_id, "content_id":content_id})
        if one_absence != None:
            up_absence = {"join":json['join']}
            client.board.absence.find_one_and_update({"_id":one_absence['_id']},{'$set': up_absence})
        else:
            json['user_id'] = ObjectId(json['user_id'])
            json['content_id'] = ObjectId(json['content_id'])
            client.board.absence.insert_one(json)
    except:
        return "エラーです"
    return 'ok'
