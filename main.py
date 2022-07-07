#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pkgutil import extend_path
from time import sleep

from bs4 import BeautifulSoup
import requests
from flask import Flask, request, jsonify, render_template, redirect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import datetime

from tables import Description

app = Flask(__name__)
# 文字化け対策
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=["GET", "POST"])
def odd_even():
    if request.method == "GET":
        return """
        <h2>偶数奇数判定APP</h2>
        下に整数を入力してください。奇数か偶数か判定します
        <form action="/" method="POST">
        <input name="num"></input>
        </form>"""
    else:
        try:
            return """
            {}は{}です！
            <form action="/" method="POST">
            <input name="num"></input>
            </form>""".format(str(request.form["num"]), ["偶数", "奇数"][int(request.form["num"]) % 2])
        except:
            return """
                    有効な数字ではありません！入力しなおしてください。
                    <form action="/" method="POST">
                    <input name="num"></input>
                    </form>"""


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

        d = {
            'title': title,
            'price': price
        }
        d_list.append(d)
        print(d)

        sleep(1)

    return jsonify(d_list)


@app.route("/scraping/amazon", methods=["GET", "POST"])
def amazon_scraping():
    if request.method == "GET":
        return """
        <h2>Amazonスクレイピング</h2>
        スクレイピングしたいワードを入力してください。
        <form action="/scraping/amazon" method="POST">
        <input name="word"></input>
        </form>"""
    else:
        try:
            uri = 'https://www.amazon.co.jp'

            print("0")
            driver = webdriver.Chrome('./chromedriver')
            print("1")
            driver.implicitly_wait(10)
            driver.get(uri)
            print("2")

            sleep(1)

            search_text = request.form["word"]
            text_box = driver.find_element("name", "field-keywords")
            text_box.send_keys(search_text)
            submit_btn = driver.find_element(By.ID, 'nav-search-submit-button')
            print("3")
            submit_btn.click()
            print("4")
            sleep(1)

            goods_list = driver.find_element(By.CSS_SELECTOR, '.sg-col-inner')
            goods_list = goods_list[:3]
            print(goods_list)

            res_list = []
            height = 1000
            today = datetime.datetime.now().strftime('%Y.%m.%d %H:%M')
            with open('Amazon' + str(today) + '.csv', 'w', encoding='UTF-8', errors='replace') as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerow(['No', '値段', '画像URL', '商品説明'])
                no = 1
                previousPrice, previousImage, previousDescription = '', '', ''
                for goods in goods_list:
                    try:
                        price = goods.find_element(
                            By.CLASS_NAME, "a-price-whole").text
                        print(price)
                    except:
                        price = '[No Price]'
                    try:
                        image = goods.find_element(
                            By.CLASS_NAME, "s-image").get_attribute("src")
                        print(image)
                    except:
                        image = '[No Image]'
                    try:
                        description = goods.find_element(
                            By.CSS_SELECTOR, ".a-size-base-plus.a-color-base.a-text-normal").text
                        print(description)
                    except:
                        description = '[No Description]'
                    if not (price == '[No Price]' and image == '[No Image]'
                            and Description == '[No Description]') and \
                        not (price == previousPrice
                             and image == previousImage and description == previousDescription):
                        writer.writerow([no, price, image, description])
                        no += 1
                        previousPrice = price
                        previousImage = image
                        previousDescription = description
                        dict = {"Price": previousPrice, "Image": previousImage,
                                "Description": previousDescription}
                        res_list.append(dict)
                    res_list.append(dict)
                    driver.execute_script(
                        "window.scrollTo(0, {});".format(height))
                    height += 500

                    sleep(1)

            driver.close()
            return """
                {}
                <form action="/" method="POST">
                <input name="word"></input>
                </form>""".format(jsonify(res_list))
        except:
            driver.close()
            return """
                再度検索する
                <form action="/scraping/amazon" method="POST">
                <input name="num"></input>
                </form>"""


@app.route("/scraping/athome", methods=["GET", "POST"])
def athome_scraping():
    if request.method == "GET":
        return """
        <h2>アットホームスクレイピング</h2>
        スクレイピングしたい都道府県を入力してください。
        <form action="/scraping/athome" method="POST">
        <input name="tdfk"></input>
        </form>"""
    else:
        try:
            root_uri = 'https://www.athome.co.jp/'

            driver = webdriver.Chrome('./chromedriver')
            driver.implicitly_wait(10)
            driver.get(root_uri)

            sleep(1)
            chuuko_ikkodate_link = driver.find_element(
                By.CLASS_NAME, "login_link")
            sleep(1)
            chuuko_ikkodate_link.click()
            print(chuuko_ikkodate_link)
            sleep(5)

            # search_text = request.form["word"]
            # text_box = driver.find_element("name", "field-keywords")
            # text_box.send_keys(search_text)
            # submit_btn = driver.find_element('id', 'nav-search-submit-button')
            # submit_btn.click()
            # sleep(1)

            # goods_list = driver.find_element(By.CSS_SELECTOR, '.sg-col-inner')
            # goods_list = goods_list[:3]
            # print(goods_list)

            # res_list = []
            # height = 1000
            # today = datetime.datetime.now().strftime('%Y.%m.%d %H:%M')
            # with open('Amazon' + str(today) + '.csv', 'w', encoding='UTF-8', errors='replace') as f:
            #     writer = csv.writer(f, lineterminator="\n")
            #     writer.writerow(['No', '値段', '画像URL', '商品説明'])
            #     no = 1
            #     previousPrice, previousImage, previousDescription = '', '', ''
            #     for goods in goods_list:
            #         try:
            #             price = goods.find_element(
            #                 By.CLASS_NAME, "a-price-whole").text
            #             print(price)
            #         except:
            #             price = '[No Price]'
            #         try:
            #             image = goods.find_element(
            #                 By.CLASS_NAME, "s-image").get_attribute("src")
            #             print(image)
            #         except:
            #             image = '[No Image]'
            #         try:
            #             description = goods.find_element(
            #                 By.CSS_SELECTOR, ".a-size-base-plus.a-color-base.a-text-normal").text
            #             print(description)
            #         except:
            #             description = '[No Description]'
            #         if not (price == '[No Price]' and image == '[No Image]'
            #                 and Description == '[No Description]') and \
            #             not (price == previousPrice
            #                  and image == previousImage and description == previousDescription):
            #             writer.writerow([no, price, image, description])
            #             no += 1
            #             previousPrice = price
            #             previousImage = image
            #             previousDescription = description
            #             dict = {"Price": previousPrice, "Image": previousImage,
            #                     "Description": previousDescription}
            #             res_list.append(dict)
            #         res_list.append(dict)
            #         driver.execute_script(
            #             "window.scrollTo(0, {});".format(height))
            #         height += 500

            # sleep(1)

            driver.close()
            return """
                {}
                <form action="/scraping/athome" method="POST">
                <input name="word"></input>
                </form>""".format(jsonify("正常"))
        except:
            driver.close()
            return """
                アットホームを再度検索する
                <form action="/scraping/athome" method="POST">
                <input name="num"></input>
                </form>"""


@app.route("/scraping/makuake", methods=["GET", "POST"])
def makuake_scraping():
    if request.method == "GET":
        return """
        <h2>マクアケスクレイピング</h2>
        スクレイピングしたいワードを入力してください。
        <form action="/scraping/makuake" method="POST">
        <input name="tdfk"></input>
        </form>"""
    else:
        try:
            # マクアケのURL
            root_uri = 'https://www.makuake.com/'

            driver = webdriver.Chrome('./chromedriver')
            driver.implicitly_wait(10)
            driver.get(root_uri)

            search_text = request.form["word"]

            sleep(1)
            search_form = driver.find_element(
                By.CLASS_NAME, "findHeaderInput")
            sleep(1)
            search_form.send_keys(search_text)
            sleep(1)
            search_btn = driver.find_element(
                By.CLASS_NAME, "findFormHeaderSubmit")
            search_btn.click()
            sleep(2)

            media_list = driver.find_element(
                By.CLASS_NAME, "media")
            print(media_list)
            sleep(2)

            # res_list = []
            # height = 1000
            # today = datetime.datetime.now().strftime('%Y.%m.%d %H:%M')
            # with open('Amazon' + str(today) + '.csv', 'w', encoding='UTF-8', errors='replace') as f:
            #     writer = csv.writer(f, lineterminator="\n")
            #     writer.writerow(['No', '値段', '画像URL', '商品説明'])
            #     no = 1
            #     previousPrice, previousImage, previousDescription = '', '', ''
            #     for goods in goods_list:
            #         try:
            #             price = goods.find_element(
            #                 By.CLASS_NAME, "a-price-whole").text
            #             print(price)
            #         except:
            #             price = '[No Price]'
            #         try:
            #             image = goods.find_element(
            #                 By.CLASS_NAME, "s-image").get_attribute("src")
            #             print(image)
            #         except:
            #             image = '[No Image]'
            #         try:
            #             description = goods.find_element(
            #                 By.CSS_SELECTOR, ".a-size-base-plus.a-color-base.a-text-normal").text
            #             print(description)
            #         except:
            #             description = '[No Description]'
            #         if not (price == '[No Price]' and image == '[No Image]'
            #                 and Description == '[No Description]') and \
            #             not (price == previousPrice
            #                  and image == previousImage and description == previousDescription):
            #             writer.writerow([no, price, image, description])
            #             no += 1
            #             previousPrice = price
            #             previousImage = image
            #             previousDescription = description
            #             dict = {"Price": previousPrice, "Image": previousImage,
            #                     "Description": previousDescription}
            #             res_list.append(dict)
            #         res_list.append(dict)
            #         driver.execute_script(
            #             "window.scrollTo(0, {});".format(height))
            #         height += 500

            # sleep(1)

            driver.close()
            return jsonify(media_list)
        except:
            driver.close()
            return """
                マクアケを再度検索する
                <form action="/scraping/makuake" method="POST">
                <input name="word"></input>
                </form>"""


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
