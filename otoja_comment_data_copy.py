# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 15:08:10 2019

@author: user
"""

from bs4 import BeautifulSoup
#import json
import requests
import csv

target_url = "https://www.youtube.com/watch?v=EXPVfeiIEmE&list=PL1Z1KdfmKueY_A2Gmx7olbDNPlMMgL1oa&index=44&t=0s"
dict_str = ""
next_url = ""
comment_data = []
comment_data2 = []
session = requests.Session()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def convert_time(input_t):
    if input_t[0] == '-':
        return 0
    t = list(map(int, input_t.split(':')))
    if len(t) == 2:
        t = 60 * t[0] + t[1]
    else:
        t = 60 * 60 * t[0] + 60 * t[1] + t[2]
    return t
# まず動画ページにrequestsを実行しhtmlソースを手に入れてlive_chat_replayの先頭のurlを入手
html = requests.get(target_url)
soup = BeautifulSoup(html.text, "html.parser")

for iframe in soup.find_all("iframe"):
    if("live_chat_replay" in iframe["src"]):
        next_url= iframe["src"]

while(1):

    try:
        html = session.get(next_url, headers=headers)
        soup = BeautifulSoup(html.text,"lxml")

        # 次に飛ぶurlのデータがある部分をfind_allで探してsplitで整形
        for scrp in soup.find_all("script"):
            if "window[\"ytInitialData\"]" in scrp.text:
                dict_str = scrp.text.split(" = ")[1]

        # javascript表記なので更に整形. falseとtrueの表記を直す
        dict_str = dict_str.replace("false","False")
        dict_str = dict_str.replace("true","True")

        # 辞書形式と認識すると簡単にデータを取得できるが, 末尾に邪魔なのがあるので消しておく（「空白2つ + \n + ;」を消す）
        dict_str = dict_str.rstrip("  \n;")
        # 辞書形式に変換
        dics = eval(dict_str)

        # "https://www.youtube.com/live_chat_replay?continuation=" + continue_url が次のlive_chat_replayのurl
        continue_url = dics["continuationContents"]["liveChatContinuation"]["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
        next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url
        # dics["continuationContents"]["liveChatContinuation"]["actions"]がコメントデータのリスト。先頭はノイズデータなので[1:]で保存
        for samp in dics["continuationContents"]["liveChatContinuation"]["actions"][1:]:
            d = {}
            try:
                comment_data.append(str(samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]+"\n"))
                comment_data2.append(str(samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"][0]["text"]+"\n"))
            except:
                print("時間取得できませんでした")
                continue
            try:
                time_msec = samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]
                d['timestamp'] = convert_time(time_msec)
                #time_msec=int(samp["replayChatItemAction"]["videoOffsetTimeMsec"])#コメントした時間のミリ秒を取得
                #time_msec.append(int(time_msec/1000))#ミリ秒→秒に変換
                time_msec.apppend(d)
                d.apppend(time_msec)

                #print(str(time_msec)+"秒")
            except:
                print("時間取得できませんでした")
                continue

           
    # next_urlが入手できなくなったら終わり
    except:
        break

# comment_data.txt にコメントデータを書き込む
with open("otoja_comment_data6.csv", mode='w', encoding="utf-8_sig") as f:
    #f.writelines(comment_data)
    #f.writelines(comment_data2)
    f.writelines(time_msec)
    f.writelines(d)
    #f.writelines(d['timestamp'])