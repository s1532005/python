# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:50:36 2019

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:22:46 2019

@author: user
"""

import sys
import os
import numpy as np
import tkinter as tk

import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as tkFileDialog

# アプリケーション（GUI）クラス
class Application(tk.Frame):
    DEBUG_LOG = True
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        # ペインウィンドウ
        # PanedWindow
        ##  orient : 配置（vertical or horizontal）
        ##  bg : 枠線の色
        # pack
        ##  expand ：可変（True or False(固定)
        ##  fill : スペースが空いている場合の動き（tk.BOTH　縦横に広がる）
        ##  side ：　配置する際にどの方向からつめていくか（side or top ・・・）
        pw_main = tk.PanedWindow(self.master, orient='horizontal')
        pw_main.pack(expand=True, fill = tk.BOTH, side="left")

        pw_left = tk.PanedWindow(pw_main, orient='vertical')
        pw_main.add(pw_left)
        # フレーム
        ##  bd ：ボーダーの幅
        ##  relief ：フレームの枠の形
        fm_select = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_select)
        ## padx , pady ：外側の横、縦の隙間
        label_fpath = tk.Label(fm_select, text="YoutubeURL", width=20)
        ## ラベルを配置
        label_fpath.grid(row=0, column=0, padx=2, pady=2)
        ##  justify：文字寄せ（center or left or right）
        ##  sticky：スペースが空いている場合の動き（tk.W + tk.E 縦横に広がる）
        entry_fpath = tk.Entry(fm_select, justify="left", width=50)
        entry_fpath.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S,padx=2, pady=2)
         ## 削除
        entry_fpath.delete( 0, tk.END ) 
        ## 先頭行に値を設定
        entry_fpath.insert( 0, "https://youtube.com/watch?v=*" )
        #値の取得
        #print('Entryの初期値を出力：{}'.format(entry_fpath.get()))
        # ボタン
        # ボタンイベントに引数を渡す
        fm_btns = tk.Frame(pw_left, bd=2, relief="ridge")
        fm_btns.pack(side="top")
        pw_left.add(fm_btns)

        btn_tool_1 = tk.Button(fm_btns, text="Hilight（上手いプレイ）集", command=lambda:self.btn_ivent("Hiligth"), width=20) 
        btn_tool_1.grid(row=1, column=0, sticky=tk.W + tk.E, padx=2, pady=10)

        btn_tool_2 = tk.Button(fm_btns, text="Funny(盛り上がり)場面集", command=lambda:self.btn_ivent("Funny"), width=20) 
        btn_tool_2.grid(row=1, column=1, sticky=tk.W + tk.E, padx=2, pady=10)
    
        btn_select_file = tk.Label(fm_btns, text="※どちらかを選択", width=15)
        btn_select_file.grid(row=1, column=10, padx=10, pady=20)

    def btn_ivent(self, msg):
        print(msg)
    
    def Hilight(self, msg):
        print(msg)
        
    def Funny(self, msg):
        print(msg)
        
    def select_file(self):
        print('now roading')

# 実行
root = tk.Tk()        
myapp = Application(master=root)
myapp.master.title("My Application") # タイトル
myapp.master.geometry("480x260") # ウィンドウの幅と高さピクセル単位で指定（width x height）

myapp.mainloop()