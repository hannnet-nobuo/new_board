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

@app.route('/index')
def index():
    if(not_login()):
        return redirect_no_login()
    url = 'http://127.0.0.1:5000/index'
    return render_template('index.html', username=session.get('username'), url=url)

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
                error = '繧ｿ繧､繝医Ν縺九Γ繝・そ繝ｼ繧ｸ縺後°繧峨〒縺吶・
            else:
                client.board.content.insert_one(content)
        except:
            error = '莠域悄縺帙〓繧ｨ繝ｩ繝ｼ縺瑚ｵｷ縺阪∪縺励◆縲・
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
            tmp['absence'] = '縺ゅｊ'
        else:
            tmp['absence'] = '縺ｪ縺・
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
                error = '繧ｿ繧､繝医Ν縺九Γ繝・そ繝ｼ繧ｸ縺後°繧峨〒縺吶・
            else:
                client.board.content.find_one_and_update({"_id":ObjectId(_id)},{'$set': content})
        except:
            error = '繧ｿ繧､繝医Ν縺九Γ繝・そ繝ｼ繧ｸ繧貞・蜉帙＠縺ｦ縺上□縺輔＞縲・
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
            error = '蜑企勁縺ｫ螟ｱ謨励＠縺ｾ縺励◆縲・
        if(error == None):
            return redirect(url_for('list'))
    content = client.board.content.find_one({"_id":ObjectId(_id)})
    if(content == None):
        return redirect(url_for('list'))
    if(content['absence'] == True):
        content['absence'] = 'checked'
    return render_template('delete.html', username=session.get('username'), error=error, content=content)

