import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
import os

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.5162 SLBChan/32'}

driver = webdriver.Chrome()

songname = '不能说的秘密'
url = 'https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord=' + songname
driver.get(url)
driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/ul[2]/li[1]/div[1]/a').click()
window_handles = driver.window_handles
driver.switch_to.window(window_handles[1])
time.sleep(1)
data = driver.page_source
soup = BeautifulSoup(data, 'lxml')
datas = soup.select('.ie8FontColor')
f = open('words.txt', 'w', encoding='utf-8')
for i in range(len(datas)):
    if len(datas[i].text) != 1:
        print(datas[i].text)
        f.write(datas[i].text)
f.close()
time.sleep(60)

