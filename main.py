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
    # 変数urlに（取得したい）ホームページのURLを格納する
    base_url = 'https://coconala.com/'
    IT_categories_url = base_url + 'categories/11?ref_c=1'
    IT_programing_categories_url = base_url + 'categories/231?ref=category_popular_subcategories'
    IT_scraping_categories_url = base_url + 'categories/230?ref_c=1&sort_by=fav'

    # 変数d_listに空のリストを作成する
    d_list = []

    # アクセスするためのURLをtarget_urlに格納する
    # for i in range(1,3)とする事で、2ページまでループが回る
    for i in range(1, 3):
        print('d_listの大きさ：', len(d_list))
        target_url = IT_programing_categories_url.format(i)

        # print()してtarget_urlを確認する
        print(target_url)

        # target_urlへのアクセス結果を変数rに格納
        r = requests.get(target_url)

        # 1ページ毎に1秒処理を止めてサーバに負荷がかからないようにする
        sleep(1)

        # 取得結果を解析してsoupに格納
        soup = BeautifulSoup(r.text)

        # 全ての物件情報（２０件）を取得する
        contents = soup.find_all('div', class_="cassetteitem")

        # 各物件情報から「物件詳細」と「各部屋情報」を取得する
        for content in contents:
            # それぞれを解析する
            detail = content.find('div', class_='cassetteitem_content')
            table = content.find('table', class_='cassetteitem_other')

            title = detail.find(
                'div', class_='cassetteitem_content-title').text
            address = detail.find('li', class_='cassetteitem_detail-col1').text
            access = detail.find('li', class_='cassetteitem_detail-col2').text
            age = detail.find('li', class_='cassetteitem_detail-col3').text

            tr_tags = table.find_all('tr', class_='js-cassette_link')

            for tr_tag in tr_tags:

                floor, price, first_fee, capacity = tr_tag.find_all('td')[2:6]

                fee, management_fee = price.find_all('li')
                deposit, gratuity = first_fee.find_all('li')
                madori, menseki = capacity.find_all('li')

                # 解析した結果を辞書に格納する
                d = {
                    'title': title,
                    'address': address,
                    'access': access,
                    'age': age,
                    'floor': floor.text,
                    'fee': fee.text,
                    'management_fee': management_fee.text,
                    'deposit': deposit.text,
                    'gratuity': gratuity.text,
                    'madori': madori.text,
                    'menseki': menseki.text
                }
                print(d_list)
                d_list.append(d)
    return jsonify(d_list)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
