import pymysql

db = pymysql.connect(host='localhost', user='root', database='music', charset='utf8', port=3306)
cur = db.cursor()
singer = '周'
sql = 'SELECT * FROM song WHERE singer LIKE "%{}%" '.format(singer)
cur.execute(sql)
data = cur.fetchall()
for da in data:
    print(da[0])

cur.close()
db.close()
