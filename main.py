#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from time import sleep

from bs4 import BeautifulSoup
import requests
from flask import Flask, jsonify, render_template
from selenium import webdriver

app = Flask(__name__)
# 文字化け対策
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=['GET'])
def test():
    return jsonify({'message': "Hello!"})


@app.route("/crowdworks_scraping", methods=['GET'])
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

        sleep(1)

    return jsonify(d_list)


@app.route("/amazon_scraping", methods=['GET'])
def amazon_scraping():
    uri = 'https://www.amazon.co.jp'

    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(10)
    driver.get(uri)

    sleep(1)

    text_box = driver.find_element("id", "twotabsearchtextbox")
    text_box.send_keys('iphone')
    submit_btn = driver.find_element('id', 'nav-search-submit-button')
    submit_btn.click()

    # 子要素のspan要素のhref属性を取得したい場合
    # e1 = driver.find_elements_by_xpath(
    #     '//div[@id="親要素のID"]/span')
    # e1.get_attribute('href')

    # e2 = driver.find_elements_by_tag_name('span')

    sleep(1)

    return jsonify()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
