#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from time import sleep
from bs4 import BeautifulSoup
import requests
from flask import Flask, request, make_response, jsonify, render_template, url_for
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import datetime
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as pyp

app = Flask(__name__)
# 文字化け対策
app.config['JSON_AS_ASCII'] = False

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/scraping/crowdworks", methods=['GET'])
def crowdworks_scraping():
    # クラウドワークスの仕事を探す
    uri = 'https://crowdworks.jp/public/jobs?category=jobs&order=score'
    d_list = []
    r = requests.get(uri)
    soup = BeautifulSoup(r.text, 'html.parser')
    contents = soup.find_all('div', class_="job_item")
    for content in contents:
        title = content.find('h3', class_='item_title').text.replace('\n', '')
        price = content.find('b', class_='amount').text.replace('\n', '')
        d = {'title': title,
            'price': price}
        d_list.append(d)
        print(d)
        sleep(1)
    return jsonify(d_list)

@app.route("/csv_upload", methods=["GET", "POST"])
def csv_upload():
    if request.method == "GET":
        return """
        <h2>CSV入出力</h2>
        <form action="/csv_upload" method="post" enctype="multipart/form-data">
           <input type="file" name="uploadFile"/>
           <input type="submit" value="submit"/>
        </form>
        <a href="{}">to top</a>""".format(url_for('index'))
    else:
        try:
            if 'uploadFile' not in request.files:
                make_response(jsonify({'result':'uploadFile is required.'}))

            upload_file = request.files['uploadFile']
            df = pd.read_csv(upload_file, encoding = "UTF-8")
            df = pd.DataFrame(df)
            df_reset=df.set_index('No')

            return """
                <h2>CSVの取り込みが完了しました。</h2>
                <form action="/csv" method="post" enctype="multipart/form-data">
                    <input type="file" name="uploadFile"/>
                    <input type="submit" value="submit"/>
                </form>
                <a href="{}">to top</a>
                {}
                """.format(url_for('index'), df_reset.to_html(justify="match-parent",header="true", table_id="table"))
        except:
            return """
                <h2>再度CSVファイルをアップロードする。</h2>
                <form action="/csv" method="post" enctype="multipart/form-data">
                    <input type="file" name="uploadFile"/>
                    <input type="submit" value="submit"/>
                </form>
                <a href="{}">to top</a>""".format(url_for('index'))

@app.route("/scraping/makuake", methods=["GET", "POST"])
def makuake_scraping():
    if request.method == "GET":
        return """
        <h2>マクアケスクレイピング</h2>
        スクレイピングしたいワードを入力してください。
        <form action="/scraping/makuake" method="POST">
            <input name="word"></input>
        </form>
        <a href="{}">to top</a>""".format(url_for('index'))
    else:
        try:
            search_text = request.form["word"]
            # マクアケのURL
            root_uri = 'https://www.makuake.com/'
            sleep(1)
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.implicitly_wait(30)
            driver.get(root_uri)
            sleep(1)
            search_form = driver.find_element(
                By.CLASS_NAME, "findHeaderInput")
            sleep(1)
            search_form.send_keys(search_text)
            sleep(3)
            search_btn = driver.find_element(
                By.CLASS_NAME, "findFormHeaderSubmit")
            search_btn.click()
            sleep(2)
            media_list = driver.find_elements(
                By.CLASS_NAME, "media")
            sleep(2)
            res_list = []
            height = 1000
            today = datetime.datetime.now().strftime('%Y.%m.%d %H:%M')
            with open('Makuake' + str(today) + '.csv', 'w', encoding='UTF-8', errors='replace') as csv_f:
                sleep(2)
                writer = csv.writer(csv_f, lineterminator="\n")
                sleep(2)
                writer.writerow(['No', '達成率', '値段', '画像URL', '商品説明'])
                no = 1
                PreviousAchievementRate, previousPrice, previousImage, previousDescription = '', '', ''
                for media in media_list:
                    try:
                        achievementRate = media.find_element(
                            By.CLASS_NAME, "media-low-bar-num").text
                        print(price)
                    except:
                        achievementRate = '[No Price]'
                    try:
                        price = media.find_element(
                            By.CSS_SELECTOR, "div.media-middle-money p").text
                        print(price)
                    except:
                        price = '[No Price]'
                    try:
                        image = media.find_element(
                            By.CLASS_NAME, "media-up-thumb").get_attribute("src")
                        print(image)
                    except:
                        image = '[No Image]'
                    try:
                        description = media.find_element(By.CLASS_NAME, "media-up-ttl").text
                        print(description)
                    except:
                        description = '[No Description]'
                    if not (achievementRate == '[No achievementRate]' and price == '[No Price]' and image == '[No Image]'
                            and description == '[No Description]') and \
                        not (achievementRate == PreviousAchievementRate and price == previousPrice
                             and image == previousImage and description == previousDescription):
                        writer.writerow([no, achievementRate, price, image, description])
                        no += 1
                        PreviousAchievementRate = achievementRate
                        previousPrice = price
                        previousImage = image
                        previousDescription = description
                        dict = {"AchievementRate": achievementRate, "Price": price, "Image": image,
                                "Description": description}
                        res_list.append(dict)
                    res_list.append(dict)
                    driver.execute_script(
                        "window.scrollTo(0, {});".format(height))
                    height += 100
                    print(height)
                    sleep(1)
            df = pd.DataFrame(res_list, encoding = "UTF-8")
            df_reset=df.set_index('No')
            driver.puit()
            return df_reset.to_html(justify="match-parent",header="true", table_id="table")
        except:
            return """
                マクアケを再度検索する
                <form action="/scraping/makuake" method="POST">
                <input name="word"></input>
                </form>
                <a href="{}">to top</a>""".format(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
