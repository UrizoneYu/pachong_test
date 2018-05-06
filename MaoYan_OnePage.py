#!/usr/bin/python
# -*- coding: utf-8 -*-
# 猫眼电影看排行榜抓取结果-单页

import requests
import re
import json

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
    # python 生成器
    for item in items:
        yield {
            'index': item[0],
            'img': item[1],
            # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
            'title': item[2].strip(),  # 去除收首尾的空格
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False)+'\n')

def main():
    url = 'http://maoyan.com/board/4'
    html = get_one_page(url)
    item = parse_one_page(html)
    # parse中添加生成器之后，需要在main方法中，变成for循环结果
    for result in item:
        write_to_file(result)

main()