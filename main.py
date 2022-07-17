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




@app.route("/csv_campfire", methods=["GET", "POST"])
def csv_campfire():
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
                <div class="text-center">
                    <h2 class="mt-4">CSV入出力</h2>
                    <div class="mt-4">
                        <form action="/csv_campfire" method="post" enctype="multipart/form-data">
                            <input type="file" name="uploadFile"/>
                            <input class="mt-3 btn btn-success btn-lg" type="submit" value="submit"/>
                        </form>
                    </div>
                </div>
                <div class="mt-3 text-right">
                    <a class="btn btn-info btn-lg mt-3" href="{}">to top</a>
                </div>
            </div>
        </body>
        </html>
        """.format(url_for('index'))
    else:
        try:
            if 'uploadFile' not in request.files:
                make_response(jsonify({'result': 'uploadFile is required.'}))

            upload_file = request.files['uploadFile']
            df = pd.read_csv(upload_file, encoding="UTF-8")
            df = pd.DataFrame(df)
            try:
                df["詳細URL"] = df["詳細URL"].map(lambda s: '<a href="{}" target="_blank">詳細ページ</a>'.format(s))
            except:
                print("変数が存在しません")
            try:
                df["リンク"] = df["リンク"].map(lambda s: '<a href="{}" target="_blank">詳細ページ</a>'.format(s))
            except:
                print("変数が存在しません")
            try:
                df["画像"] = df["画像"].map(lambda s: "<img src='{}' width='200' />".format(s))
            except:
                print("変数が存在しません")
            try:
                df["画像URL"] = df["画像URL"].map(lambda s: "<img src='{}' width='200' />".format(s))
            except:
                print("変数が存在しません")
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
                    <div class="text-center">
                        <h4 class="mt-4">CSV表示</h4>
                        <form action="/csv_campfire" method="post" enctype="multipart/form-data">
                            <div class="mt-4">
                                <input type="file" name="uploadFile"/>
                                <input class="mt-3 btn btn-success btn-lg" type="submit" value="submit"/>
                            </div>
                        </form>
                    </div>
                    <div class="my-3 text-right">
                        <a class="btn btn-info btn-lg mt-3" href="{}">to top</a>
                    </div>
                    {}
                </div>
            </body>
            </html>
            """.format(url_for('index'), df.to_html(classes=["table", "table-bordered", "table-hover"], escape=False, justify="match-parent", header="true", table_id="table"))
        except:
            return """
                <h2>再度CSVファイルをアップロードする。</h2>
                <form action="/csv_campfire" method="post" enctype="multipart/form-data">
                    <input type="file" name="uploadFile"/>
                    <input type="submit" value="submit"/>
                </form>
                <a href="{}">to top</a>""".format(url_for('index'))

@app.route("/scraping/campfire", methods=["GET", "POST"])
def campfire():
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
                <div class="text-center">
                    <h4 class="mt-4">キャンプファイヤー</h4>
                    <form action="/scraping/campfire" method="POST">
                        <div class="mt-4">
                            新着情報を取得する
                            <input class="px-3 py-2" type="submit" value="submit"/>
                            <p class="mt-3" style="color:red">※情報の取得に数分かかります。</p>
                        </div>
                    </form>
                </div>
                <div class="mt-3 text-right">
                    <a class="btn btn-info btn-lg mt-3" href="{}">to top</a>
                </div>
            </div>
        </body>
        </html>
        """.format(url_for('index'))
    else:
        try:
            root_uri = 'https://camp-fire.jp/'
            r = requests.get(root_uri)
            soup = BeautifulSoup(r.text, 'html.parser')
            fresh_wrap = soup.find('section', class_="fresh")
            freshes = fresh_wrap.find_all('div', class_="box")
            # AchievementRate, Price, Rest, Description, Url, Image = [], [], [], [], [], []
            res_list = []
            for fresh in freshes:
                achievementRates = fresh.select("div.meter-in div span")
                achievementRates = fresh.select("div.meter-in div span")
                prices = fresh.select("div.total")
                rests = fresh.select("div.rest")
                descriptions = fresh.select("div.box-title a h4")
                urls = fresh.select("div.box-title a")
                images = fresh.select("img.lazyload")

                achievementRate = achievementRates[0].string
                price = prices[0].getText().replace('\n', '').replace('現在', '')
                rest = rests[0].getText().replace('\n', '').replace('支援者', '')
                description = descriptions[0].string
                get_url = urls[0].attrs['href']
                url = root_uri + get_url
                image = images[0].attrs['data-src']

                dict = {"達成率": achievementRate,
                        "金額": price,
                        "支援者": rest,
                        "内容": description,
                        "リンク": url,
                        "画像": image
                        }
                res_list.append(dict)
                sleep(2)
            df = pd.DataFrame(res_list)
            print(df.columns)
            today = datetime.datetime.now().strftime('%Y.%m.%d %H:%M')
            df[["達成率","金額","支援者","内容","リンク","画像"]].to_csv('Campfire' + str(today) + '.csv', index=False, encoding='utf_8_sig')
            df["リンク"] = df["リンク"].map(lambda s: '<a href="{}" target="_blank">詳細ページ</a>'.format(s))
            df["画像"] = df["画像"].map(lambda s: "<img src='{}' width='200' />".format(s))
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
                        <div class="text-center">
                            <h2 class="mt-4">キャンプファイヤー</h2>
                            <p  class="mt-4" style="color:green">スプレイピングが完了しました！</p>
                            <form action="/scraping/campfire_ranking" method="POST">
                                <div class="mt-4">
                                    もう一度取得する
                                    <input class="px-3 py-2" type="submit" value="submit"/>
                                    <p class="mt-3" style="color:red">※情報の取得に数分かかります。</p>
                                </div>
                            </form>
                        </div>
                        <div class="mt-3 text-right">
                            <a class="btn btn-info btn-lg my-3" href="{}">to top</a>
                        </div>
                        {}
                    </div>
                </body>
                </html>
                """.format(url_for('index'), df.to_html(classes=["table", "table-bordered", "table-hover"], escape=False, justify="match-parent", header="true", table_id="table"))
        except:
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
                        <div class="text-center">
                            <h2 class="mt-3">campfire</h2>
                            <p>エラーが発生しました。</p>
                            <form action="/scraping/campfire" method="POST">
                                <input type="submit" value="submit"/>
                            </form>
                        </div>
                        <a class="btn btn-info btn-lg my-3" href="{}">to top</a>
                    </div>
                </body>
                </html>""".format(url_for('index'))

# @app.route("/scraping/makuake", methods=["GET", "POST"])
# def makuake_scraping():
#     if request.method == "GET":
#         return """
#         <!doctype html>
#         <html lang="ja">
#         <head>
#             <meta charset="utf-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
#             <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
#         </head>
#         <body>
#             <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
#             <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
#             <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
#             <div class="container">
#                 <h2 class="mt-3">マクアケスクレイピング</h2>
                
#                 <form action="/scraping/makuake" method="POST">
#                     <div class="mt-3">
#                         <p>スクレイピングしたいワードを入力してください。</p>
#                         <input name="word"></input>
#                     </div>
#                     <div class="mt-3">
#                         <input class="px-3 py-2" type="submit" value="submit"/>
#                     </div>
#                 </form>
#                 <div class="mt-3 text-right">
#                     <a class="btn btn-info btn-lg mt-3" href="{}">to top</a>
#                 </div>
#             </div>
#         </body>
#         </html>
#         """.format(url_for('index'))
#     else:
#         try:
#             search_text = request.form["word"]
#             root_uri = 'https://www.makuake.com/'
#             sleep(1)
#             driver = webdriver.Chrome(ChromeDriverManager().install())
#             driver.implicitly_wait(30)
#             driver.get(root_uri)
#             sleep(1)
#             search_form = driver.find_element(
#                 By.CLASS_NAME, "findHeaderInput")
#             sleep(1)
#             search_form.send_keys(search_text)
#             sleep(3)
#             search_btn = driver.find_element(
#                 By.CLASS_NAME, "findFormHeaderSubmit")
#             search_btn.click()
#             sleep(2)
#             res_dict_list = []
#             i = 0
#             while True:
#                 try:
#                     media_list = driver.find_elements(
#                     By.CLASS_NAME, "pj-box-li")
#                     sleep(2)
#                     height = 100
#                     print("2")
#                     today = datetime.datetime.now().strftime('%Y.%m.%d %H:%M')
#                     print("3")
#                     with open('Makuake' + str(today) + '.csv', 'w', encoding='UTF-8', errors='replace') as csv_f:
#                         sleep(2)
#                         print("4")
#                         writer = csv.writer(csv_f, lineterminator="\n")
#                         sleep(2)
#                         writer.writerow(['No', '達成率', '値段', '商品説明', 'リンク', '画像'])
#                         no = 1
#                         PreviousAchievementRate, previousPrice, previousDescription, previousUrl, previousImage = '', '', '', '', ''
                        
#                         print("4.5")
#                         for media in media_list:
#                             print("5")
#                             try:
#                                 achievementRate = media.find_element(
#                                     By.CLASS_NAME, "media-low-bar-num").text
#                             except:
#                                 achievementRate = '[No Price]'
#                             try:
#                                 price = media.find_element(
#                                     By.CSS_SELECTOR, "div.media-middle-money p").text
#                             except:
#                                 price = '[No Price]'
#                             try:
#                                 description = media.find_element(
#                                     By.CLASS_NAME, "media-up-ttl").text
#                             except:
#                                 description = '[No Description]'
#                             try:
#                                 url = media.find_element(
#                                     By.CLASS_NAME, "media-up").get_attribute("href")
#                             except:
#                                 url = '[No Url]'
#                             try:
#                                 image = media.find_element(
#                                     By.CLASS_NAME, "media-up-thumb").get_attribute("src")
#                             except:
#                                 image = '[No Image]'
#                             if not (achievementRate == '[No achievementRate]' and price == '[No Price]' and image == '[No Image]'
#                                     and description == '[No Description]' and url == '[No Url]') and \
#                                 not (achievementRate == PreviousAchievementRate and price == previousPrice
#                                     and image == previousImage and description == previousDescription and url == previousUrl):
#                                 print("6")
#                                 writer.writerow(
#                                     [no, achievementRate, price, description, url, image])
#                                 no += 1
#                                 print("7")
#                                 PreviousAchievementRate = achievementRate
#                                 previousPrice = price
#                                 previousUrl = url
#                                 previousDescription = description
#                                 previousImage = image
#                                 dict = {"AchievementRate": achievementRate,
#                                         "Price": price,
#                                         "Image": image,
#                                         "Description": description,
#                                         "Url": url
#                                         }
#                                 res_dict_list.append(dict)
#                             print("8")
#                             driver.execute_script(
#                                 "window.scrollTo(0, {});".format(height))
#                             height += 50
#                             print(height)
#                             sleep(2)
#                     print("9")
#                     print(i)
#                     i = i + 1
#                     print(i)
#                     next_btn = driver.find_element(By.XPATH, '//a[@rel="next"]')
#                     next_btn.click()
#                     sleep(2)
#                     if i >= 2:
#                         break
#                 except NoSuchElementException:
#                     driver.quit()
#                     break
#             print("10")
#             sleep(5)
#             df = pd.DataFrame(res_dict_list)
#             df["Url"] = df["Url"].map(lambda s: '<a href="{}" target="_blank">詳細ページ</a>'.format(s))
#             df["Image"] = df["Image"].map(lambda s: "<img src='{}' width='200' />".format(s))
#             driver.quit()
#             return """
#                 <!doctype html>
#                 <html lang="ja">
#                 <head>
#                     <meta charset="utf-8">
#                     <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
#                     <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
#                 </head>
#                 <body>
#                     <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
#                     <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
#                     <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
#                     <div class="container">
#                         <h2 class="mt-3">マクアケスクレイピング</h2>
#                         スプレイピングが完了しました！
#                         <form action="/scraping/makuake" method="POST">
#                             <input name="word"></input>
#                             <input type="submit" value="submit"/>
#                         </form>
#                         <a class="btn btn-info btn-lg my-3" href="{}">to top</a>
#                         {}
#                     </div>
#                 </body>
#                 </html>
#                 """.format(url_for('index'), df.to_html(classes=["table", "table-bordered", "table-hover"], escape=False, justify="match-parent", header="true", table_id="table"))
#         except:
#             return """
#                 <!doctype html>
#                 <html lang="ja">
#                 <head>
#                     <meta charset="utf-8">
#                     <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
#                     <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
#                 </head>
#                 <body>
#                     <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
#                     <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
#                     <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
#                     <div class="container">
#                         <h2 class="mt-3">マクアケスクレイピング</h2>
#                         <p>エラーが発生しました。マクアケを再度検索する。</p>
#                         <form action="/scraping/makuake" method="POST">
#                             <input name="word"></input>
#                             <input type="submit" value="submit"/>
#                         </form>
#                         <a class="btn btn-info btn-lg my-3" href="{}">to top</a>
#                         {}
#                     </div>
#                 </body>
#                 </html>""".format(url_for('index'))

# @app.route("/scraping/crowdworks", methods=['GET'])
# def crowdworks_scraping():
#     try:
#         uri = 'https://crowdworks.jp/public/jobs?category=jobs&order=score'
#         d_list = []
#         r = requests.get(uri)
#         soup = BeautifulSoup(r.text, 'html.parser')
#         contents = soup.find_all('div', class_="job_item")
#         for content in contents:
#             title = content.find('h3', class_='item_title').text.replace('\n', '')
#             price = content.find('b', class_='amount').text.replace('\n', '')
#             d = {'title': title,
#                 'price': price}
#             d_list.append(d)
#             print(d)
#             sleep(1)
#         return """
#             <h2>完了</h2>
#             <a href="{}">to top</a>
#             {}
#             """.format(url_for('index'), jsonify(d_list))
#     except:
#         return """
#             <h2>エラー</h2>
#             <a href="{}">to top</a>""".format(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
