#!/usr/bin/python
# -*- coding: utf-8 -*-
# 猫眼电影看排行榜抓取结果-分页

import requests
import time
import csv
import re

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_one_page(html):
    pattern = re.compile(
             '<dd>.*?board-index.*?">(.*?)</i>.*?<img data-src="(.*?)".*?class="name.*?data-val=.*?">(.*?)</a></p>.*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>.*?</div>.*?class="integer">(.*?)</i>.*?class="fraction">(.*?)</i>', re.S)
    items = re.findall(pattern, html)
    movies =[]
    for item in items:
        rank = item[0]
        img = item[1]
        # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
        name = item[2].strip() # 去除收首尾的空格
        people = item[3].strip()[3:] if len(item[3]) > 3 else ''
        date = item[4].strip()[5:] if len(item[4]) > 5 else ''
        score = item[5].strip() + item[6].strip()
        data = [rank, img, name, people, date, score]
        movies.append(data)
    with open('result.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        for re1 in movies:
            print(re1)
            writer.writerow(re1)

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    parse_one_page(html)


if __name__ == '__main__':
    with open('result.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['排行', '图片地址', '影片', '主要演员', '放映时间', '得分'])
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)