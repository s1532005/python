# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 15:08:10 2019

@author: user
"""

from bs4 import BeautifulSoup
import requests

#　targert_urlにURLを書き込む
target_url = "https://www.youtube.com/watch?v="
dict_str = ""
next_url = ""
comment_data = []
time_data = []
session = requests.Session()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

# まず動画ページにrequestsを実行しhtmlソースを手に入れてlive_chat_replayの先頭のurlを入手
html = requests.get(target_url)
soup = BeautifulSoup(html.text, "html.parser")

def convert_time(input_t):
    if input_t[0] == '-':
        return 0
    t = list(map(int, input_t.split(':')))
    if len(t) == 2:
        t = 60 * t[0] + t[1]
    else:
        t = 60 * 60 * t[0] + 60 * t[1] + t[2]
    return t

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
            try:
                t=(str(samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"])+"\n")
                d = convert_time(t)
                e = str(d)
                time_data.append(e + "：")
            except:
                print("時間取得失敗")
                continue
            try:
                comment_data.append(str(samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"][0]["text"]+"\n"))
            except:
                print("コメント取得失敗")
                continue
    # next_urlが入手できなくなったら終わり
    except:
        break
# ファイル名を入力、コメントデータの書き込み
with open(".csv", mode='w', encoding="utf-8_sig") as f:         
    f.writelines(time_data)
    f.writelines(comment_data)
