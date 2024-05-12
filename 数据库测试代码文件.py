from flask import Flask, render_template, request, flash
import pymysql

db = pymysql.connect(host='localhost', user='root', database='User', charset='utf8', port=3306)
cur = db.cursor()

username = 'user'
sql = 'SELECT * FROM user '
cur.execute(sql)
dbuser = cur.fetchall()[py]
print(dbuser)

cur.close()
db.close()
