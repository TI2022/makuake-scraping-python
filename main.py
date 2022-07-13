#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from time import sleep
from bs4 import BeautifulSoup
import requests
from flask import Flask, request, make_response, jsonify, render_template, url_for
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import datetime
import numpy as np
import pandas as pd

# import matplotlib as mpl
# import matplotlib.pyplot as pyp

app = Flask(__name__)
# 文字化け対策
app.config['JSON_AS_ASCII'] = False

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/scraping/crowdworks", methods=['GET'])
def crowdworks_scraping():
    if request.method == "GET":
        return """
        <h2>クラウドワークス</h2>
        <form action="/scraping/crowdworks" method="post" enctype="multipart/form-data">
           <input name="word"></input>
           <input type="submit" value="submit"/>
        </form>
        <a href="{}">to top</a>""".format(url_for('index'))
    else:
        try:
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

            return """
                <h2>CSVの取り込みが完了しました。</h2>
                <form action="/scraping/crowdworks" method="post" enctype="multipart/form-data">
                    <input type="file" name="uploadFile"/>
                    <input type="submit" value="submit"/>
                </form>
                <a href="{}">to top</a>
                {}
                """.format(url_for('index'), jsonify(d_list))
        except:
            return """
                <h2>再度CSVファイルをアップロードする。</h2>
                <form action="/scraping/crowdworks" method="post" enctype="multipart/form-data">
                    <input type="file" name="uploadFile"/>
                    <input type="submit" value="submit"/>
                </form>
                <a href="{}">to top</a>""".format(url_for('index'))

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
                make_response(jsonify({'result': 'uploadFile is required.'}))

            upload_file = request.files['uploadFile']
            df = pd.read_csv(upload_file, encoding="UTF-8")
            df = pd.DataFrame(df)
            df_reset = df.set_index('No')

            return """
                <h2>CSVの取り込みが完了しました。</h2>
                <form action="/csv_upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="uploadFile"/>
                    <input type="submit" value="submit"/>
                </form>
                <a href="{}">to top</a>
                {}
                """.format(url_for('index'), df_reset.to_html(justify="match-parent", header="true", table_id="table"))
        except:
            return """
                <h2>再度CSVファイルをアップロードする。</h2>
                <form action="/csv_upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="uploadFile"/>
                    <input type="submit" value="submit"/>
                </form>
                <a href="{}">to top</a>""".format(url_for('index'))


@app.route("/scraping/makuake", methods=["GET", "POST"])
def makuake_scraping():
    if request.method == "GET":
        return """
        <!doctype html>
        <html lang="ja">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
        </head>
        <body>
            <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
            <div class="container">
                <h2 class="mt-3">マクアケスクレイピング</h2>
                
                <form action="/scraping/makuake" method="POST">
                    <div class="mt-3">
                        <p>スクレイピングしたいワードを入力してください。</p>
                        <input name="word"></input>
                    </div>
                    <div class="mt-3">
                        <input class="px-3 py-2" type="submit" value="submit"/>
                    </div>
                </form>
                <div class="mt-3 text-right">
                    <a class="btn btn-info btn-lg mt-3" href="{}">to top</a>
                </div>
            </div>
        </body>
        </html>
        """.format(url_for('index'))
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
            res_dict_list = []
            i = 0
            while True:
                try:
                    media_list = driver.find_elements(
                    By.CLASS_NAME, "pj-box-li")
                    sleep(2)
                    height = 100
                    print("2")
                    today = datetime.datetime.now().strftime('%Y.%m.%d %H:%M')
                    print("3")
                    with open('Makuake' + str(today) + '.csv', 'w', encoding='UTF-8', errors='replace') as csv_f:
                        sleep(2)
                        print("4")
                        writer = csv.writer(csv_f, lineterminator="\n")
                        sleep(2)
                        writer.writerow(['No', '達成率', '値段', '商品説明', '詳細URL', '画像'])
                        no = 1
                        PreviousAchievementRate, previousPrice, previousDescription, previousUrl, previousImage = '', '', '', '', ''
                        
                        print("4.5")
                        for media in media_list:
                            print("5")
                            try:
                                achievementRate = media.find_element(
                                    By.CLASS_NAME, "media-low-bar-num").text
                            except:
                                achievementRate = '[No Price]'
                            try:
                                price = media.find_element(
                                    By.CSS_SELECTOR, "div.media-middle-money p").text
                            except:
                                price = '[No Price]'
                            try:
                                description = media.find_element(
                                    By.CLASS_NAME, "media-up-ttl").text
                            except:
                                description = '[No Description]'
                            try:
                                url = media.find_element(
                                    By.CLASS_NAME, "media-up").get_attribute("href")
                            except:
                                url = '[No Url]'
                            try:
                                image = media.find_element(
                                    By.CLASS_NAME, "media-up-thumb").get_attribute("src")
                            except:
                                image = '[No Image]'
                            if not (achievementRate == '[No achievementRate]' and price == '[No Price]' and image == '[No Image]'
                                    and description == '[No Description]' and url == '[No Url]') and \
                                not (achievementRate == PreviousAchievementRate and price == previousPrice
                                    and image == previousImage and description == previousDescription and url == previousUrl):
                                print("6")
                                writer.writerow(
                                    [no, achievementRate, price, description, url, image])
                                no += 1
                                print("7")
                                PreviousAchievementRate = achievementRate
                                previousPrice = price
                                previousUrl = url
                                previousDescription = description
                                previousImage = image
                                dict = {"AchievementRate": achievementRate,
                                        "Price": price,
                                        "Image": image,
                                        "Description": description,
                                        "Url": url
                                        }
                                res_dict_list.append(dict)
                            print("8")
                            driver.execute_script(
                                "window.scrollTo(0, {});".format(height))
                            height += 50
                            print(height)
                            sleep(2)
                    print("9")
                    print(i)
                    i = i + 1
                    print(i)
                    next_btn = driver.find_element(By.XPATH, '//a[@rel="next"]')
                    next_btn.click()
                    sleep(2)
                    if i >= 2:
                        break
                except NoSuchElementException:
                    driver.quit()
                    break
            print("10")
            sleep(5)
            df = pd.DataFrame(res_dict_list)
            df["Url"] = df["Url"].map(lambda s: '<a href="{}" target="_blank">{}</a>'.format(s,s))
            df["Image"] = df["Image"].map(lambda s: "<img src='{}' width='200' />".format(s))
            driver.quit()
            return """
                <!doctype html>
                <html lang="ja">
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
                </head>
                <body>
                    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
                    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
                    <div class="container">
                        <h2 class="mt-3">マクアケスクレイピング</h2>
                        スプレイピングが完了しました！
                        <form action="/scraping/makuake" method="POST">
                            <input name="word"></input>
                            <input type="submit" value="submit"/>
                        </form>
                        <a class="btn btn-info btn-lg my-3" href="{}">to top</a>
                        {}
                    </div>
                </body>
                </html>
                """.format(url_for('index'), df.to_html(classes=["table", "table-bordered", "table-hover"], escape=False))
        except:
            return """
                エラーが発生しました。マクアケを再度検索する。
                <form action="/scraping/makuake" method="POST">
                <input name="word"></input>
                </form>
                <a href="{}">to top</a>""".format(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
