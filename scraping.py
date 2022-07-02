# coding:utf-8

# スクレイピング先のサーバに負荷をかけないように処理を一時的に止められるsleepをインポート
from time import sleep

# 要素を取得しやすくするBeautifulSoupをインポート
from bs4 import BeautifulSoup
# requestsはスクレイピング先のURLを取得し、HTML要素を取得する為にインポートする
import requests
# pandasはスクレイピングした結果をグラフ化など人が見やすくなるように変換するためにインポートし、pdで呼び出す
import pandas as pd

# 変数urlに（取得したい）ホームページのURLを格納する
url = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}'
# 変数d_listに空のリストを作成する
d_list = []

# アクセスするためのURLをtarget_urlに格納する
# for i in range(1,3)とする事で、2ページまでループが回る
for i in range(1, 3):
    print('d_listの大きさ：', len(d_list))
    target_url = url.format(i)

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

        title = detail.find('div', class_='cassetteitem_content-title').text
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

            d_list.append(d)

# d_listの２番目まで中身を確認する
# d_list[:2]

# 変数d_listを使って、データフレームを作成する
# df = pd.DataFrame(d_list)

# データフレームの先頭５行を確認する
# df.head()

# dfの大きさを確認する
# df.shape

# 物件名の重複を削除して、その大きさを確認する
# len(df.title.unique())

# to_csv()を使って、データフレームをCSV出力する
# df.to_csv('test.csv', index=None, encoding='utf-8-sig')
