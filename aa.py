# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 16:17:43 2019

@author: user
"""

import tkinter, tkinter.messagebox

# Tkクラス生成
tki = tkinter.Tk()
# 画面サイズ
tki.geometry('300x200')
# 画面タイトル
tki.title('ラジオボタン')

# ラジオボタンのラベルをリスト化する
rdo_txt = ['Python','Java','C#']
# ラジオボタンの状態
rdo_var = tkinter.IntVar()

# ラジオボタンを動的に作成して配置
for i in range(len(rdo_txt)):
    rdo = tkinter.Radiobutton(tki, value=i, variable=rdo_var, text=rdo_txt[i]) 
    rdo.place(x=50, y=30 + (i * 24))

# ボタンクリックイベント
def btn_click():
    num = rdo_var.get()
    tkinter.messagebox.showinfo('チェックされた項目', rdo_txt[num])

# ボタン作成 
btn = tkinter.Button(tki, text='ラジオボタン取得', command=btn_click)
btn.place(x=100, y=170) 
tki.mainloop()
