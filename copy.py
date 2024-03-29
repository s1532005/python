# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 18:20:38 2019

@author: user
"""

from bs4 import BeautifulSoup
import json
import requests

target_url = "https://www.youtube.com/watch?v=AILrIqsvXpQ"
dict_str = ""
next_url = ""
comment_data = []
session = requests.Session()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

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
        # dics['continuationContents']['liveChatContinuation']['actions']がコメントデータのリスト．先頭はノイズデータなので[1:]で保存
        for samp in dics['continuationContents']['liveChatContinuation']['actions'][1:]:
            d = {}
            try:
                samp = samp['replayChatItemAction']['actions'][0]['addChatItemAction']['item']
                chat_type = list(samp.keys())[0]
                if 'liveChatTextMessageRenderer' == chat_type:
                    # 通常チャットの処理
                    if 'simpleText' in samp['liveChatTextMessageRenderer']['message']:
                        d['message'] = samp['liveChatTextMessageRenderer']['message']['simpleText']
                    else:
                        d['message'] = ''
                        for elem in samp['liveChatTextMessageRenderer']['message']['runs']:
                            if 'text' in elem:
                                d['message'] += elem['text']
                            else:
                                d['message'] += elem['emoji']['shortcuts'][0]
                    t = samp['liveChatTextMessageRenderer']['timestampText']['simpleText']
                    d['timestamp'] = convert_time(t)
                    d['id'] = samp['liveChatTextMessageRenderer']['authorExternalChannelId']
                elif 'liveChatPaidMessageRenderer' == chat_type:
                    # スパチャの処理
                    if 'simpleText' in samp['liveChatPaidMessageRenderer']['message']:
                        d['message'] = samp['liveChatPaidMessageRenderer']['message']['simpleText']
                    else:
                        d['message'] = ''
                        for elem in samp['liveChatPaidMessageRenderer']['message']['runs']:
                            if 'text' in elem:
                                d['message'] += elem['text']
                            else:
                                d['message'] += elem['emoji']['shortcuts'][0]
                    t = samp['liveChatPaidMessageRenderer']['timestampText']['simpleText']
                    d['timestamp'] = convert_time(t)
                    d['id'] = samp['liveChatPaidMessageRenderer']['authorExternalChannelId']
                elif 'liveChatPaidStickerRenderer' == chat_type:
                    # コメントなしスパチャ
                    continue
                elif 'liveChatLegacyPaidMessageRenderer' == chat_type:
                    # 新規メンバーメッセージ
                    continue
                elif 'liveChatPlaceholderItemRenderer' == chat_type:
                    continue
                else:
                    print('知らないチャットの種類' + chat_type)
                    continue
            except Exception:
                # print(Exception.args)
                continue
            comment_data.append(d)
    return comment_data

def convert_time(input_t):
    if input_t[0] == '-':
        return 0
    t = list(map(int, input_t.split(':')))
    if len(t) == 2:
        t = 60 * t[0] + t[1]
    else:
        t = 60 * 60 * t[0] + 60 * t[1] + t[2]
    return t


def find_highlight(comment_data, interval, grass_num, margin):
    '''
    interval この秒数以内であれば同一の見どころ
    grass_num 見どころとする草コメント数
    margin はじめて草コメントがあった箇所からマージンを取る
    authorExternalChannelId
    '''
    time = -11
    cnt = 0
    point = []
    client = set()
    for c in comment_data:
        m = c['message']
        if m[-1] == '草' or m[-1] == 'w':
            cnt += 1
            if c['timestamp'] - time > interval:
                time = c['timestamp']
                point.append([time, 1])
            else:
                time = c['timestamp']
                point[-1][1] += 1
        client.add(c['id'])

    # pprint.pprint(point)

    # 投稿するコメントを生成
    comment = ''
    for c in point:
        if c[1] > grass_num:
            comment += (inverse_convert_time(c[0], margin) + f' 草×{c[1]}\n')
    total = len(comment_data)
    minute_speed = len(comment_data) / (comment_data[-1]['timestamp'] / 60)
    minute_speed = round(minute_speed, 2)
    comment += f'\nコメント数 {total}\n草コメント数 {cnt}\n1分あたりのコメント数 {minute_speed}\nコメントした人数 {len(client)}'
    return comment


def inverse_convert_time(t, margin):
    if t - margin > 0:
        m, s = divmod(t - margin, 60)
        h, m = divmod(m, 60)
    else:
        m, s = divmod(t, 60)
        h, m = divmod(m, 60)

    if h > 0:
        return f'{h:.0f}:{m:02.0f}:{s:02.0f}'
    else:
        return f'{m:.0f}:{s:02.0f}'


def parse():
    parser = ArgumentParser()

    parser.add_argument('url', help='youtubeのurl', type=str)
    parser.add_argument('-i', help='次の草コメントを受け付ける時間', default=5, type=int)
    parser.add_argument('-g', help='これ以上の草コメントを抽出する', default=5, type=int)
    parser.add_argument('-m', help='m秒前の地点をみどころの開始地点とする', default=15, type=int)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse()

    if not os.path.isdir('comment'):
        pathlib.Path('comment')
    filename = 'comment/' + args.url.split('=')[1] + '.txt'
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            # comment_data = ast.literal_eval(f.read())
            reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
            comment_data = list(reader)
    else:
        comment_data = get_comment(args.url)
        with open(filename, 'w') as f:
            # f.write(str(comment_data))
            writer = csv.DictWriter(
                f, ['timestamp', 'message', 'id'], quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerows(comment_data)

    comment = find_highlight(comment_data, args.i, args.g - 1, args.m)
    pyperclip.copy(comment)
    print(comment)