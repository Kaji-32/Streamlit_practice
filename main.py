from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import requests as re
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
import streamlit as st
import datetime

#Streamlitのページ設定
st.set_page_config(
    page_title ='Streamlitテストページ：ゴルフラウンド平均飛距離',
    page_icon ='⛳️',
)

st.title('ゴルフ一打目〜カップインまでの平均飛距離を計測します。')

#ゴルフ場、日にち、ティーグラウンドを取得
golf_hole = st.text_input('ラウンドしたゴルフ場名を記載してください','奈良万葉カントリークラブ')
dt_now = datetime.datetime.now()
golh_date = st.date_input(
        'ラウンドした日にち',
        dt_now,
        max_value=dt_now)
tie_choice = st.radio(
    'ティーグラウンド',
    ('Blue','White','Red'))

st.info(golf_hole)
st.info(golh_date)
st.info(tie_choice)
btn_golf = st.button('よろしいですか？',on_click='しばらくお待ちください')
if btn_golf == True:
    #静的操作に変更するマジックコマンド
    options = Options()
    options.add_argument('--headless')

    #ブラウザの立ち上げ(オプション設定にしているためバックグラウンドで操作するようになっている)
    driver = webdriver.Chrome(options=options)

    #ゴルフサイト
    driver.get('https://reserve.golfdigest.co.jp/kinki/')

    #ゴルフ場の検索を行う
    search_box = driver.find_element_by_name('transform')
    search_box.send_keys(golf_hole)
    sleep(2)
    search_box.send_keys(Keys.ENTER)
    sleep(2)

    #検索結果のゴルフ場の詳細画面に遷移する
    golf_element = driver.find_element_by_xpath('//*[@id="list"]/div[1]/h3/a')

    #JavaScriptを直接叩くことにより遷移を行える
    driver.execute_script('document.querySelector("#list > div.course.calendar1 > h3 > a").click();')
    sleep(2)
    driver.execute_script('document.querySelector("#tab-navi > div > ul > li:nth-child(3) > a").click();')
    sleep(2)
    url = driver.current_url

    #リクエストにURLを入力する
    res = re.get(url)
    soup = bs(res.text, 'html.parser')

    #タイトル抽出
    hole_column = soup.find_all('td')
    if tie_choice == 'Blue':
        for i in range(1,9):
            golf_Blue_list = [
                [hole_column[i].text,hole_column[i+10].text],
                [hole_column[i+60].text,hole_column[i+70].text],
            ]
            print(golf_Blue_list)
    elif tie_choice =='White':
        for i in range(1,9):
            print(f'{hole_column[i].text}\t{hole_column[i+20].text}\t\t{hole_column[i+60].text}\t{hole_column[i+80].text}')
    elif tie_choice =='Red':
        for i in range(1,9):
            print(f'{hole_column[i].text}\t{hole_column[i+40].text}\t\t{hole_column[i+60].text}\t{hole_column[i+100].text}')








