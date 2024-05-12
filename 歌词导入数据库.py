import os
import re
import time
import requests
import threading
import multiprocessing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine
import pymysql

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
cur = conn.cursor()

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.5162 SLBChan/32'}

sql = "select song from song"
cur.execute(sql)
songdatas = cur.fetchall()




def findwords(length1, length2):
    for k in range(length1, length2):
        songname = songdatas[k][0]
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        driver = webdriver.Chrome(options=option)
        try:
            url = 'https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord=' + songname
            driver.get(url)
            driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/ul[2]/li[1]/div[1]/a').click()
            window_handles = driver.window_handles
            driver.switch_to.window(window_handles[1])
            time.sleep(3)
            data = driver.page_source
            soup = BeautifulSoup(data, 'lxml')
            datas = soup.select('.ie8FontColor')
            words = ''
            for j in range(len(datas)):
                if len(datas[j].text) != 1:
                    words = words + datas[j].text
            sql1 = "update song set words = '{}' where song like '%{}%'".format(words, songname)
            cur.execute(sql1)
            conn.commit()
            print("'{}'插入数据成功".format(songname))
        except:
            pass
            print("'{}'插入数据失败".format(songname))


def test(length1, length2):
    try:
        findwords(length1, length2)
    except:
        print('插入失败')


if __name__ == '__main__':
    number = len(songdatas)
    LB = [0, int(number / 4), int(number / 2), int(number / 4 * 3), number]
    multiprocessing_list = []

    for i in range(4):
        t = multiprocessing.Process(target=test, args=(LB[i], LB[i + 1]))
        multiprocessing_list.append(t)

    for i in multiprocessing_list:
        i.start()

    for i in multiprocessing_list:
        i.join()


