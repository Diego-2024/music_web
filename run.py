from flask import Flask, render_template, request,flash, send_file
import pymysql
from 验证码 import *



app = Flask(__name__)
app.secret_key = 'fsh12345678'

@app.route('/')
def index():
    return  render_template('select.html')

@app.route('/login')
def login():
    # image, code = get_verify_code()
    # image_path = 'static/images/yzm.png'
    # image.save(image_path)
    # # session['image'] = code
    # return render_template('login.html', image=image, code=code)
    return  render_template('login.html')

@app.route('/get_code_image')
def get_code_image():
    image, code = get_verify_code()
    image_path = 'static/images/yzm1.png'
    image.save(image_path)
    # session['image'] = code
    return send_file(image_path, mimetype='image/png'), 200


@app.route('/select',methods=['GET', 'POST'] )
def select():
    db = pymysql.connect(host='localhost', user='root', database='music', charset='utf8', port=3306)
    cur = db.cursor()
    if request.method == 'POST':
        if request.form['song']:
            song = request.form['song']
            sql = 'SELECT * FROM song WHERE song LIKE "%{}%" '.format(song)
            cur.execute(sql)
            datas = cur.fetchall()
            return render_template('music.html', datas = datas)
        else:
            singer = request.form['singer']
            sql = 'SELECT * FROM song WHERE singer LIKE "%{}%" '.format(singer)
            cur.execute(sql)
            datas = cur.fetchall()
            return render_template('music.html', datas = datas)
    return render_template('select.html')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    db = pymysql.connect(host='localhost', user='root', database='user', charset='utf8', port=3306)
    cur = db.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # checkcode = request.form['checkcode']
        if True:
        # if checkcode.lower() == session['image'].lower():
            sql = 'SELECT * FROM user WHERE user = "{}" '.format(username)
            cur.execute(sql)
            dbuser = cur.fetchall()[0]
            if username == dbuser[0] and password == dbuser[1]:
                return  render_template('select.html', username=username, password=password)
            else :
                flash('账户或密码不正确', 'danger')
        else :
            flash('验证码不正确', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['first-password']
        second_password = request.form['second-password']
        db = pymysql.connect(host='localhost', user='root', database='user', charset='utf8', port=3306)
        cur = db.cursor()
        sql = 'SELECT * FROM user '
        cur.execute(sql)
        datas = cur.fetchall()[0]
        if user in datas:
            flash('该账号已经存在', 'danger')
            return render_template('register.html')
        else:
            if password == second_password:
                sql = " INSERT INTO user (user, password) VALUES ('{}', '{}')".format(user, password)
                cur.execute(sql)
                db.commit()
                flash('注册成功', 'danger')
                return render_template('register.html')
            else:
                flash('前后两次密码不一致', 'danger')
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

cur.close()
db.close()