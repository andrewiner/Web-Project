from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import re
import pymysql
import traceback
import random
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:X,xw126929@localhost:3306/user?charset=utf8'

db = SQLAlchemy(app)

config1 = {
    'host': 'localhost', 'user': 'root', 'password': 'X,xw126929', 'database': 'user', 'charset': 'utf8', 'port': 3306  # 注意端口为int 而不是str
}


global db1
db1 = pymysql.connect(**config1)
######################################################################################################################
global login_username, login_judge, iflogin, userid
login_username = ""
login_judge = 0
iflogin = 0
userid = -1
######################################################################################################################
global register_username, register_password1, register_password2, register_judge
register_username = ""
register_password1 = ""
register_password2 = ""
register_judge = 0
global res, restore
res = []
restore = []


class userinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))


@app.route('/')
def index():
    global iflogin, login_username, login_judge, register_judge, register_password1, register_password2, userid
    login_judge = 0
    register_judge = 0
    register_password1 = ""
    register_password2 = ""

    global res

    class subject:
        __slots__ = ('id', 'href', 'cover_href', 'title', 'plot', 'basicinfo')

        def __init__(self, id: int, href: str, cover_href: str, title: str, plot: str, basicinfo: str):
            self.id = id
            self.href = href
            self.cover_href = cover_href
            self.title = title
            self.plot = plot
            self.basicinfo = basicinfo

    sl = []
    for i in range(48):
        with open('static/data/' + str(i) + '/title.txt', encoding='UTF-8') as f:
            title = f.read()
        with open('static/data/' + str(i) + '/plot.txt', encoding='UTF-8') as f:
            plot = f.read()
            plot = re.sub('\n', '<br />', plot)
            plot = re.sub('    ', '&emsp;&emsp;', plot)
        with open('static/data/' + str(i) + '/basicinfo.txt', encoding='UTF-8') as f:
            basicinfo = f.read()
            basicinfo = re.sub('\n', '<br />', basicinfo)
            basicinfo = re.sub('    ', '&emsp;&emsp;', basicinfo)
        sl.append(subject(i, '', 'static/data/' + str(i) + '/picture.jpg', title, plot, basicinfo))
    if iflogin == 1:
        dbname = "`" + str(userid) + "`"
        db1.ping(reconnect=True)
        cursor = db1.cursor()
        sql = "SELECT `collect` FROM " + dbname + ";"
        cursor.execute(sql)
        store = cursor.fetchall()
        if store == None:
            flag = 0
        else:
            flag = 1
        db1.close()
    else:
        flag = 2
        store = []
    store1 = []
    for item in store:
        store1.append(int(item[0]))
    return render_template('index.html', login_username=login_username, navigation=sl, store=store1, flag=flag, iflogin=iflogin)


@app.route('/addsearch', methods=['POST'])
def addsearch():
    global res
    searchresult = request.form['search']
    if len(searchresult) > 40:
        searchresult = searchresult[0:40]
    words = []
    chi = []
    eng = []
    searchresult = re.sub(r'[^\w\s]', '', searchresult)
    searchresult = re.sub('[_]', '', searchresult)
    english = (re.sub('[\u4e00-\u9fa5]', '', searchresult)).lower()
    english = re.sub('[0-9]', '', english)
    chinese = re.sub('[a-zA-Z]', '', searchresult)
    chinese = re.sub(' ', '', chinese)

    for i in range(0, len(chinese) + 1):
        for j in range(i + 1, len(chinese) + 1):
            chi.append(chinese[i:j])

    backupeng = []
    backupeng = re.sub(' ', '', english)
    n = 0
    if backupeng != "":
        while n < len(english):
            for j in range(n, len(english)):
                if (english[j] == ' ' or j == len(english) - 1) and n != j:
                    if(j == len(english) - 1):
                        j = j + 1
                    words.append(english[n:j])
                    n = j + 1
                    break
        for word in words:
            for i in range(0, len(word) + 1):
                for j in range(i + 1, len(word) + 1):
                    eng.append(word[i:j])
    chi = list(set(chi))
    eng = list(set(eng))
    chi = sorted(chi, key=lambda i: len(i), reverse=True)
    eng = sorted(eng, key=lambda i: len(i), reverse=True)
    res = []  # 结果
    subject_num = 48  # 条目
    # 检索
    for j in chi:
        for i in range(subject_num):
            with open('static/data/' + str(i) + '/title.txt', encoding='UTF-8') as f:
                txt = f.read()
                if j in txt and i not in res:
                    res.append(i)
    for j in eng:
        for i in range(subject_num):
            with open('static/data/' + str(i) + '/title.txt', encoding='UTF-8') as f:
                txt = f.read()
                if j in txt.lower() and i not in res:
                    res.append(i)
                    break
    return redirect(url_for('result'))
###################################################################################################################################################


@app.route('/login')
def login():
    global login_username, login_judge, iflogin, userid
    action = url_for('addlogin')
    return render_template('login.html', name=login_username, login_judge=login_judge, act=action)


@app.route('/addlogin', methods=['POST'])
def addlogin():
    global login_username, login_judge, userid, iflogin
    username = request.form['username_lgin']
    password = request.form['password_lgin']
    try:
        v = userinfo.query.filter_by(username=username, password=password).one()
        userid = v.id
        login_judge = 0
        iflogin = 1
        return redirect(url_for('index'))

    except:
        login_username = username
        login_judge = 1
        return redirect(url_for('login'))
#####################################################################################################################################################


@app.route('/register')
def register():
    global register_username, register_password1, register_password2, register_judge
    act1 = url_for('addregisterjudge')
    act2 = url_for('addregister')
    return render_template('register.html', name=register_username, register_judge=register_judge, password=register_password1, passworden=register_password2, act1=act1, act2=act2)


@app.route('/addregisterjudge', methods=['POST'])
def addregisterjudge():
    global register_username, register_judge, register_password1, register_password2
    register_username = request.form['username_regi']
    try:
        register_password1 = request.form['password_regi']
    except:
        register_password1 = ""
    try:
        register_password2 = request.form['password_ensure']
    except:
        register_password2 = ""
    try:
        v = userinfo.query.filter_by(username=register_username).one()
        register_judge = 1
    except:
        register_judge = 2
    return redirect(url_for('register'))


@app.route('/addregister', methods=['POST'])
def addregister():
    global register_username, register_judge, register_password1, register_password2
    username = request.form['username_regi']
    password = request.form['password_regi']
    global db1
    infolist = userinfo(username=username, password=password)
    db.session.add(infolist)
    db.session.commit()
##################################################收    藏##############################################################

    infos = userinfo.query.filter_by(username=username).one()
    num = infos.id
    dbname = "`" + str(num) + "`"
    db1.ping(reconnect=True)
    cursor = db1.cursor()
    sql = "CREATE TABLE `user`." + dbname + "(`id` INT AUTO_INCREMENT,`collect` VARCHAR(10),PRIMARY KEY (`id`));"
    try:
        cursor.execute(sql)
    except:
        traceback.print_exc()
        db1.rollback()
    db1.close()
###############################################################################################################################
    return redirect(url_for('login'))


@app.route('/result')
def result():
    global res, iflogin, userid

    class subject:
        __slots__ = ('id', 'href', 'cover_href', 'title', 'plot', 'basicinfo')

        def __init__(self, id: int, href: str, cover_href: str, title: str, plot: str, basicinfo: str):
            self.id = id
            self.href = href
            self.cover_href = cover_href
            self.title = title
            self.plot = plot
            self.basicinfo = basicinfo

    sl = []
    for i in res:
        with open('static/data/' + str(i) + '/title.txt', encoding='UTF-8') as f:
            title = f.read()
        with open('static/data/' + str(i) + '/plot.txt', encoding='UTF-8') as f:
            plot = f.read()
            plot = re.sub('\n', '<br />', plot)
            plot = re.sub('    ', '&emsp;&emsp;', plot)
        with open('static/data/' + str(i) + '/basicinfo.txt', encoding='UTF-8') as f:
            basicinfo = f.read()
            basicinfo = re.sub('\n', '<br />', basicinfo)
            basicinfo = re.sub('    ', '&emsp;&emsp;', basicinfo)
        sl.append(subject(i, '', 'static/data/' + str(i) + '/picture.jpg', title, plot, basicinfo))
    if iflogin == 1:
        dbname = "`" + str(userid) + "`"
        db1.ping(reconnect=True)
        cursor = db1.cursor()
        sql = "SELECT `collect` FROM " + dbname + ";"
        cursor.execute(sql)
        store = cursor.fetchall()
        if store == None:
            flag = 0
        else:
            flag = 1
        db1.close()
    else:
        flag = 2
        store = []
    store1 = []
    for item in store:
        store1.append(int(item[0]))
    return render_template('result.html', res=res, navigation=sl, flag=flag, store=store1, iflogin=iflogin)


@app.route('/content/<int:content_id>')
def content(content_id):
    global iflogin, db1
    outid = content_id

    class subject:
        __slots__ = ('id', 'href', 'cover_href', 'title', 'plot', 'basicinfo')

        def __init__(self, id: int, href: str, cover_href: str, title: str, plot: str, basicinfo: str):
            self.id = id
            self.href = href
            self.cover_href = cover_href
            self.title = title
            self.plot = plot
            self.basicinfo = basicinfo
    with open('static/data/' + str(outid) + '/title.txt', encoding='UTF-8') as f:
        title = f.read()
    with open('static/data/' + str(outid) + '/plot.txt', encoding='UTF-8') as f:
        plot = f.read()
        plot = re.sub('\n', '<br />', plot)
        plot = re.sub('    ', '&emsp;&emsp;', plot)
    with open('static/data/' + str(outid) + '/basicinfo.txt', encoding='UTF-8') as f:
        basicinfo = f.read()
        basicinfo = re.sub('\n', '<br />', basicinfo)
        basicinfo = re.sub('    ', '&emsp;&emsp;', basicinfo)
    content = subject(outid, '', '../static/data/' + str(outid) + '/picture.jpg', title, plot, basicinfo)
    if iflogin == 1:
        dbname = "`" + str(userid) + "`"
        db1.ping(reconnect=True)
        cursor = db1.cursor()
        sql = "SELECT `collect` FROM " + dbname + "WHERE collect=" + str(content_id) + ";"
        cursor.execute(sql)
        v = cursor.fetchone()
        if v == None:
            flag = 0
        else:
            flag = 1
        db1.close()
    else:
        flag = 2
    return render_template('content.html', content=content, id=outid, flag=flag)


@app.route('/personal')
def personal():
    global iflogin, userid

    class subject:
        __slots__ = ('id', 'href', 'cover_href', 'title', 'plot', 'basicinfo')

        def __init__(self, id: int, href: str, cover_href: str, title: str, plot: str, basicinfo: str):
            self.id = id
            self.href = href
            self.cover_href = cover_href
            self.title = title
            self.plot = plot
            self.basicinfo = basicinfo

    dbname = "`" + str(userid) + "`"
    db1.ping(reconnect=True)
    cursor = db1.cursor()
    sql = "SELECT `collect` FROM " + dbname + ";"
    cursor.execute(sql)
    store = cursor.fetchall()
    store1 = []
    for item in store:
        store1.append(int(item[0]))
    sl = []
    for i in store1:
        with open('static/data/' + str(i) + '/title.txt', encoding='UTF-8') as f:
            title = f.read()
        with open('static/data/' + str(i) + '/plot.txt', encoding='UTF-8') as f:
            plot = f.read()
            plot = re.sub('\n', '<br />', plot)
            plot = re.sub('    ', '&emsp;&emsp;', plot)
        with open('static/data/' + str(i) + '/basicinfo.txt', encoding='UTF-8') as f:
            basicinfo = f.read()
            basicinfo = re.sub('\n', '<br />', basicinfo)
            basicinfo = re.sub('    ', '&emsp;&emsp;', basicinfo)
        sl.append(subject(i, '', 'static/data/' + str(i) + '/picture.jpg', title, plot, basicinfo))

    return render_template('personal.html', navigation=sl, iflogin=iflogin)


@app.route('/addstore', methods=['POST'])
def addstore():
    global db1, userid
    act = request.form['act']
    act = int(act)
    content_id = request.form['content_id']
    db1.ping(reconnect=True)
    dbname = "`" + str(userid) + "`"
    content_id = int(content_id)
    identifier = str(content_id)
    cursor = db1.cursor()
    sql1 = "SELECT `id`, count(*) FROM" + dbname + ";"
    newid = 10000
    try:
        cursor.execute(sql1)
        v = cursor.fetchone()
        newid = v[1] + 1
    except:
        traceback.print_exc()
        db1.rollback()
    sql = "INSERT INTO " + dbname + " (`id`,`collect`) VALUES ('" + str(newid) + "','" + identifier + "');"
    try:
        cursor.execute(sql)
        db1.commit()
    except:
        traceback.print_exc()
        db1.rollback()
    db1.close()
    if act == 1:
        return redirect(url_for('content', content_id=content_id))
    elif act == 2:
        return redirect(url_for('index'))
    elif act == 3:
        return redirect(url_for('result'))


@app.route('/cancelstore', methods=['POST'])
def cancelstore():
    global db1, userid
    act = request.form['act']
    act = int(act)
    content_id = request.form['content_id']
    db1.ping(reconnect=True)
    dbname = "`" + str(userid) + "`"
    content_id = int(content_id)
    identifier = str(content_id)
    cursor = db1.cursor()
    sql = "DELETE FROM " + dbname + "WHERE `collect`='" + identifier + "';"
    sql1 = "SET @i := 0;"
    sql2 = "UPDATE " + dbname + " SET `id`= (@i:=(@i + 1));"
    try:
        cursor.execute(sql)
        db1.commit()
    except:
        traceback.print_exc()
        db1.rollback()
    cursor.execute(sql1)
    cursor.execute(sql2)
    db1.commit()
    db1.close()
    if act == 1:
        return redirect(url_for('content', content_id=content_id))
    elif act == 2:
        return redirect(url_for('index'))
    elif act == 3:
        return redirect(url_for('result'))
    elif act == 4:
        return redirect(url_for('personal'))


@app.route('/logout')
def logout():
    global login_username, login_judge, iflogin, userid
    login_username = ""
    login_judge = 0
    iflogin = 0
    userid = -1
    global register_username, register_password1, register_password2, register_judge
    register_username = ""
    register_password1 = ""
    register_password2 = ""
    register_judge = 0
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
