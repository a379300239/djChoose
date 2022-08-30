import os
import copy
import time

from imgTool.imgTool import screenShoot,imgSearch,imgCut,wordReg
from PIL import Image
import pyautogui
from mttkinter import mtTkinter as tk
from tkinter import StringVar,Label,Button,Frame
import re

global cr,noClickList


# 选择教室
class choose_room(object):
    def __init__(self):
        self.crTb = tk.Tk()
        self.crTb.geometry("300x100")  # 设置窗口大小
        self.crTb.geometry("+1300+100")  # 设置窗口显示位置
        self.crTb.attributes("-topmost", True)  # 窗口最前

        self.f1 = Frame(self.crTb)
        self.f2 = Frame(self.crTb)

        self.inf = StringVar()
        self.inf.set('开始点击')

    def layout(self):

        self.f1.pack()

        la1 = Label(self.f1, textvariable=self.inf, font=('', 20, ''), pady='10', fg='red')
        la1.pack()

        button1 = Button(self.f1,text='确认',command=startChoose_press)
        button1.pack()

    def changeInf(self, s):
        self.inf.set(s)

    def destroy(self):
        self.crTb.destroy()

    def run(self):
        self.crTb.mainloop()

    def layoutEnd(self):

        self.f1.destroy()
        self.f2.pack()

        la2 = Label(self.f2, text='选择完毕', font=('', 20, ''), pady='10', fg='red')
        la2.pack()

        button2 = Button(self.f2,text='确认',command=self.crTb.quit)
        button2.pack(side='left',padx=30)

        button3 = Button(self.f2, text='查看未点击项', command=self.showNoClick)
        button3.pack(padx=30)

    def showNoClick(self):
        os.system('notepad allFile/erro.txt')

def chooseAroom(room):
    filePath = 'allFile/img/' + room + '.jpg'

    # 截屏与读取目标教室图片
    scr = screenShoot()
    target = Image.open(filePath)

    # showImg(target)

    # 找到目标位置
    loc = imgSearch(scr, target)

    if loc != None:
        loc = loc['rectangle'][0]
    else:
        # 图像识别没找到
        return 'No'

    # 截取同一行
    width = scr.size[0]
    height = target.size[1]
    imRow = imgCut(scr,0,loc[1],width,loc[1]+height)

    # 文字识别，确认识别是否准确
    imRow.save('cache.jpg')
    wordAns = wordReg('cache.jpg')

    if room in wordAns:
        try:
            # 找到选择框
            checkBox = Image.open('allFile/img/checkbox.jpg')
            cboxLoc = imgSearch(imRow,checkBox)['rectangle'][0]

            # 获得选择框中心点并点击
            cbxLocX = cboxLoc[0] + checkBox.size[0] / 2
            cbxLocY = loc[1] + cboxLoc[1] + checkBox.size[1] / 2
            pyautogui.click(cbxLocX,cbxLocY,duration=0.1)

            # 向左移动100像素并点击，取消点击
            pyautogui.moveRel(-100, 0, duration=0.1)
            pyautogui.click()

            # 记录当前教室已点击
            global noClickList
            noClickList.remove(room)
        except: # 已经选择或无选择框，则不进行点击
            pass
    else:
        # 文字未找到
        return 'No'


def getRoom():
    with open('allFile/courseList.txt','r',encoding='utf-8') as rfile:
        s = rfile.read()

    courseS = [i.replace('主楼','') for i in re.findall(r'主楼\d{3}',s)]

    global noClickList
    noClickList = copy.deepcopy(courseS)

    return courseS

def chooseRoom(roomList):
    global noClickList
    maxPageNum = 10
    step = 1500

    for room in roomList:
        pageTime = 0

        # 选择room
        for i in range(maxPageNum):
            inf = chooseAroom(room)

            # 当前页面没有，翻页
            if inf == 'No':
                pyautogui.scroll(-1*step)
                pageTime+=1
                # 延时
                time.sleep(1.5)
            else:
                break

        # 未成功点击才上翻
        if room in noClickList:
            pyautogui.scroll(pageTime*step)

    # 写入erro.txt
    writeErro(noClickList)

    cr.layoutEnd()

def writeErro(l):
    with open('allFile/erro.txt','w') as rfile:
        for i in l:
            rfile.write(i+'\n')

def showInf(s):
    global cr

    cr.changeInf(s)

def startChoose_press():
    roomList = getRoom()

    chooseRoom(roomList)

def startChoose():
    global cr
    cr = choose_room()
    cr.layout()