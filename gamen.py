import tkinter as tk   # python3
#import Tkinter as tk   # python

TITLE_FONT = ("Helvetica", 18, "bold")

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #self.create_widgets()

        self.frames = {}
        for F in (StartPage, Hiligth集, 面白場面集):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Hiligth集",
                            command=lambda: controller.show_frame("Hiligth集"))
        button2 = tk.Button(self, text="Go to 面白場面集",
                            command=lambda: controller.show_frame("面白場面集"))
        button1.pack()
        button2.pack()
        
    def create_widgets(self):
        abel_fpath = tk.Label(fm_select, text="ファイルパス(入力)", width=20)
        ## ラベルを配置
        label_fpath.grid(row=0, column=0, padx=2, pady=2)
        entry_fpath = tk.Entry(fm_select, justify="left", width=50)
        entry_fpath.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S,padx=2, pady=2)
         ## 削除
        entry_fpath.delete( 0, tk.END ) 
        ## 先頭行に値を設定
        entry_fpath.insert( 0, "https://youtube.com/watch?v=*" )


class Hiligth集(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is Hiligth集", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class 面白場面集(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is 面白場面集", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()