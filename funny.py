# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 12:18:21 2019

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
        label_fpath = tk.Label(fm_select, text="Funny", width=40)
        label_fpath.grid(row=0, column=0, padx=2, pady=2)
        
        label_fpath = tk.Label(fm_select, text="動画切り抜き時間", width=40)
        label_fpath.grid(row=1, column=0, padx=2, pady=2)
        rdo1 = tk.Radiobutton(tk, text='Python')
        rdo1.place(x=70, y=40)
        
        label_fpath = tk.Label(fm_select, text="切り抜き数（デフォルト5か所）", width=40)
        label_fpath.grid(row=2, column=0, padx=2, pady=2)

        label_fpath = tk.Label(fm_select, text="1カットの切り抜き時間（デフォルト２分）", width=40)
        label_fpath.grid(row=3, column=0, padx=2, pady=2)
        
        
root = tk.Tk()        
myapp = Application(master=root)
myapp.master.title("My Application") # タイトル
myapp.master.geometry("480x260") # ウィンドウの幅と高さピクセル単位で指定（width x height）

myapp.mainloop()