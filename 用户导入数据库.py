import os
import re

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import pandas as pd

app = Flask(__name__)

# MySQL所在主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名，自己设置
USERNAME = "root"
# 连接MySQL的密码，自己设置
PASSWORD = ""
# MySQL上创建的数据库名称
DATABASE = "music"
# 通过修改以下代码来操作不同的SQL比写原生SQL简单很多 --》通过ORM可以实现从底层更改使用的SQL
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

db = SQLAlchemy(app)

engine = create_engine("mysql+pymysql://root:@localhost:3306/song")
conn = pymysql.connect(host='localhost', user='root', database='music', charset='utf8', port=3306)
c = conn.cursor()

for f in os.scandir(r'E:\python\music test\index\static\music'):
    try:
        song = re.findall(r'.*?-(.*?).mp3', f.name)[0]
        singer = re.findall('(.*?)-.*?', f.name)[0]
        path = '../static/music/' + f.name
        sql = "insert into song (song, singer, path) VALUES (%s, %s, %s)"
        value = (song, singer, path)
        c.execute(sql, value)
        conn.commit()
        print("插入数据成功")
        print(song, ' - ', singer)

    except IndexError:
        song = f.name
        singer = '未知歌手'
        path = '../static/music/' + f.name
        sql = "insert into song (song, singer, path) VALUES (%s, %s, %s)"
        value = (song, singer, path)
        c.execute(sql, value)
        conn.commit()
        print("插入数据成功")
        # print(song, ' - ', singer)
    except:
        pass




# 创建数据表类

# class Song(db.Model):
#     song = db.Column(db.String(125), nullable=False, primary_key=True)
#     singer = db.Column(db.String(125))
#     path = db.Column(db.String(125), nullable=False)
#
#
# @app.route('/')
# def base():  # put application's code here
#     db.create_all()
#     return 'ok'
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

# for f in os.scandir(r'E:\python\music test\index\static\music'):
#     song = re.findall('.*?-(.*?).mp3', f.name)[0]
#     singer = re.findall('(.*?)-.*?', f.name)[0]
#     path = '../static/music/' + f.name
#     print(singer, ' - ', song, ' - ', path)

c.close()
conn.close()