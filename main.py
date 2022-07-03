#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# スクレイピング先のサーバに負荷をかけないように処理を一時的に止められるsleepをインポート
from time import sleep

# 要素を取得しやすくするBeautifulSoupをインポート
from bs4 import BeautifulSoup
# requestsはスクレイピング先のURLを取得し、HTML要素を取得する為にインポートする
import requests
# pandasはスクレイピングした結果をグラフ化など人が見やすくなるように変換するためにインポートし、pdで呼び出す
import pandas as pd

# import joblib
from flask import Flask, jsonify
# import pandas as pd
# from sklearn import datasets

app = Flask(__name__)
# 文字化け対策
app.config['JSON_AS_ASCII'] = False

@app.route("/", methods=['GET'])
def test():
    return jsonify({'message': "Hello!"})

@app.route("/scraping", methods=['GET'])
def scraping():
    uri = 'https://crowdworks.jp/public/jobs?category=jobs&order=score'

    d_list = []

    r = requests.get(uri)

    soup = BeautifulSoup(r.text, 'html5lib')
    contents = soup.find_all('div', class_="job_item")
    print(contents)

    for content in contents:
        title = content.find('h3', class_='item_title').text
        price = content.find('b', class_='amount').text

        d = {
            'title': title,
            'price': price
        }
        d_list.append(d)

        sleep(2)

    return jsonify(d_list)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
