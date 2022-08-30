from mttkinter import mtTkinter as tk
from tkinter import *
import os
from initSetting.setImg import *
from choose.chooseRoom import *

class main_class(object):
    def __init__(self):
        self.tb = tk.Tk()
        self.tb.geometry("+1300+100")  # 设置窗口显示位置
        self.tb.attributes("-topmost", True)  # 窗口最前

    # 主窗口布局函数
    def layout(self):

        f1 = Frame(self.tb)
        f1.pack()

        init_button = Button(f1, text='开始列表截图', command=self.init_img,width = 20,height=5)
        init_button.pack(side='left',padx=30,pady = 30)

        startChoose_button = Button(f1, text='开始点击', command=self.to_chooseRoom,width = 20,height=5)
        startChoose_button.pack(padx=30,pady = 30)

        f2 = Frame(self.tb)
        f2.pack()

        oepn_initFile_button = Button(f2,text = '列表设置',command = self.open_initFile,width = 20,height=5)
        oepn_initFile_button.pack(side='left', padx=30, pady=10)

        open_coureseList_button = Button(f2, text='点击列表设置', command=self.open_coureseList, width=20, height=5)
        open_coureseList_button.pack(side='left', padx=30, pady=10)

    # 初始化
    def init_img(self):
        self.tb.destroy()
        startLis()

    # 选择教室
    def to_chooseRoom(self):

        self.tb.destroy()
        startChoose()

    # 打开初始化文件
    def open_initFile(self):
        os.system('notepad allFile/settings.txt')

    # 上课教室设置
    def open_coureseList(self):
        os.system('notepad allFile/courseList.txt')

    def run(self):
        self.tb.mainloop()


if __name__ == '__main__':
    m = main_class()

    m.layout()

    m.run()