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
    content = client.board.content.find_one({"_id":ObjectId(_id)})
    if(content == None):
        return "掲示板が存在しません"
    users = client.board.user.find()
    absences = client.board.absence.find_one({"content_id":ObjectId(_id)})
    disp_absences = []
    for user in users:
        one_absence = [x for x in absences if x['user_id'] == ObjectId(user['_id'])][0]
        temp_absence = {}
        temp_absence['user_id'] = user['_id']
        temp_absence['name'] = user['name']
        temp_absence['attend'] = ''
        if(one_absence != None and one_absence['attend'] == True):
            temp_absence['attend'] = 'checkted'

    return render_template('index.html',
                                    username=session.get('username'), 
                                    msg=content['msg'].replace('\n', '<br>').replace('\r', ''),
                                    absences=disp_absences)

@app.route('/new', methods=['GET','POST'])
def new():
    if(not_login()):
        return redirect_no_login()
    error = None
    content = {}
    if request.method == 'POST':
        post_absence = False
        if('absence' in request.form):
            post_absence = True
        try:
            post_title = request.form['title']
            post_msg = request.form['msg']
            content = {"title":post_title,"msg":post_msg,"absence":post_absence}
            if(post_title == '' or post_msg == ''):
                error = 'タイトルか内容が空です'
            else:
                client.board.content.insert_one(content)
        except:
            error = '予期せぬエラーが起きました'
        if(error == None):
            return redirect(url_for('list'))
        if(content['absence'] == True):
            content['absence'] = 'checked'
    return render_template('new.html', username=session.get('username'), error=error, content=content)

@app.route('/list')
def list():
    if(not_login()):
        return redirect_no_login()
    contents = []
    tmp = {}
    for content in client.board.content.find():
        tmp = {}
        tmp['msg'] = content['msg'].replace('\n', '<br>').replace('\r', '')
        tmp['title'] = content['title']
        if (content['absence'] == True):
            tmp['absence'] = 'あり'
        else:
            tmp['absence'] = 'なし'
        tmp['_id'] = content['_id']
        contents.append(tmp)
    return render_template('list.html', username=session.get('username'), contents=contents)

@app.route('/edit/<_id>', methods=['GET','POST'])
def edit(_id):
    if(not_login()):
        return redirect_no_login()
    error = None
    content = {}
    if request.method == 'POST':
        post_absence = False
        if('absence' in request.form):
            post_absence = True
        try:
            post_title = request.form['title']
            post_msg = request.form['msg']
            content = {"title":post_title,"msg":post_msg,"absence":post_absence}
            if(post_title == '' or post_msg == ''):
                error = 'タイトルかメチE��ージがからです、E
            else:
                client.board.content.find_one_and_update({"_id":ObjectId(_id)},{'$set': content})
        except:
            error = 'タイトルかメチE��ージを�E力してください、E
        if(error == None):
            return redirect(url_for('list'))
    else:
        content = client.board.content.find_one({"_id":ObjectId(_id)})
        if(content == None):
            return redirect(url_for('list'))
    if(content['absence'] == True):
        content['absence'] = 'checked'
    return render_template('edit.html', username=session.get('username'), error=error, content=content)

@app.route('/delete/<_id>', methods=['GET','POST'])
def delete(_id):
    if(not_login()):
        return redirect_no_login()
    error = None
    if request.method == 'POST':
        try:
            post_id = request.form['_id']
            client.board.content.delete_one({"_id":ObjectId(post_id)})
        except:
            error = '削除に失敗しました、E
        if(error == None):
            return redirect(url_for('list'))
    content = client.board.content.find_one({"_id":ObjectId(_id)})
    if(content == None):
        return redirect(url_for('list'))
    if(content['absence'] == True):
        content['absence'] = 'checked'
    return render_template('delete.html', username=session.get('username'), error=error, content=content)

