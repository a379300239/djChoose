import pynput
import threading
import pyautogui
from mttkinter import mtTkinter as tk
from tkinter import StringVar,Label,Button
import json

global mouseListener,keyListener    # 键鼠监听
global pressStatue                  # 状态记录
global imgNum                       # 图片
global locList                      # 位置记录
global iniC                         # 操作窗口
global classRoomDic                 # 配置信息

pressStatue = 0
imgNum = 1
locList = []

# 初始化
class init_class(object):
    def __init__(self):

        self.tbInit = tk.Tk()
        self.tbInit.geometry("500x135")             # 设置窗口大小
        self.tbInit.geometry("+1300+100")             # 设置窗口显示位置
        self.tbInit.attributes("-topmost", True)    # 窗口最前

        # 提示区文字
        self.noteInf = StringVar()
        self.noteInf.set('提示区')

        # 状态区文字
        self.statueInf = StringVar()
        self.statueInf.set('状态区')

    def layout(self):
        la1 = Label(self.tbInit,textvariable=self.noteInf,font=('',20,''),pady='10',fg = 'red')
        la1.pack()

        la2 = Label(self.tbInit, textvariable=self.statueInf, font=('',15,''),pady='10')
        la2.pack()

        useInf = '''撤回一步:右alt\t退出：esc'''
        la3 = Label(self.tbInit, text=useInf, font=("黑体",12,""))
        la3.pack(pady='5')

    def changeNoteInf(self,s):
        self.noteInf.set(s)

    def changeStatueInf(self,s):
        self.statueInf.set(s)

    def destroy(self):
        self.tbInit.quit()


# 开始监听鼠标
def startMouseLis():
    global mouseListener
    with pynput.mouse.Listener(on_click=onClick) as mouseListener:
        mouseListener.join()

# 开始监听键盘
def startKeyboardLis():
    global keyListener
    with pynput.keyboard.Listener(on_press=onPress) as keyListener:
        keyListener.join()

def locList_append(x,y):
    global locList

    if len(locList) == 2:
        locList = []

    locList.append([x, y])

def locList_pop():
    global locList
    if locList != []:
        locList.pop()

def locList_show():
    global locList
    return str(locList)

# 点击时
def onClick(x, y, button, pressed):
    global pressStatue,imgNum

    if imgNum == 0:
        imgNum = 1

    if pressed:
        if str(button) == 'Button.left' and pressStatue == 0:    # 第一个点
            # 保存第一个点坐标，并改变状态
            locList_append(x,y)
            next_pressStatue()

            showNoteInf('获得第{}张图，第一个点({},{})'.format(imgNum, x, y))      # 提示

        elif str(button) == 'Button.left' and pressStatue == 1:  # 第二个点
            # 保存第二个点坐标，改变状态，截屏
            locList_append(x,y)
            next_pressStatue()

            showNoteInf('获得第{}张图，第二个点({},{})'.format(imgNum, x, y))    # 提示

            # 向右移动100像素并点击后再截屏
            pyautogui.moveRel(100,0,duration=0.1)
            pyautogui.click()

            fileName = classRoomDic[str(imgNum)] + '.jpg'
            prtSc(locList,fileName)

            imgNum += 1

        elif str(button) == 'Button.left' and pressStatue == 2:  # 第三个点
            next_pressStatue()


# 键盘按下时
def onPress(key):
    global imgNum

    # 按esc键结束
    if str(key) == 'Key.esc':
        endLis()

    # 按右alt撤销
    if str(key) == 'Key.alt_gr':
        revoke()

        showNoteInf('撤销当前操作,{},{}'.format(locList_show(), imgNum))                   # 提示

# 撤销
def revoke():
    global pressStatue, imgNum

    # if imgNum > 0 and locList_show() != '[]':
    # 撤回上一步操作
    locList_pop()

    # 需要撤回第一个操作时 imgNum-1
    if pressStatue == 0:
        imgNum -= 1

        if imgNum<0:
            imgNum = 0

    if imgNum!=0:
        previous_pressStatue()

    # showNoteInf(locList_show())

# pressStatue下一个状态
def next_pressStatue():
    global pressStatue

    pressStatue = (pressStatue+1) % 3

# pressStatue上一个状态
def previous_pressStatue():
    global pressStatue

    # showNoteInf(pressStatue)

    if pressStatue == 0:
        pressStatue = 1

    elif pressStatue == 1:
        pressStatue = 0

    # showNoteInf(pressStatue)

# 截图
def prtSc(loc,fileName):
    if len(loc) != 2:
        return
    # 坐标转化
    x = min(loc[0][0],loc[1][0])
    y = min(loc[0][1],loc[1][1])
    rowDi = abs(loc[1][0]-loc[0][0])
    colDi = abs(loc[1][1]-loc[0][1])

    img = pyautogui.screenshot(region=(x,y,rowDi,colDi))

    img_save(img,fileName)

    global iniC
    iniC.changeStatueInf('已保存{},({},{})-({},{})'.format(fileName,loc[0][0],loc[0][1],loc[1][0],loc[1][1])) # 提示

# 保存图像
def img_save(img,fileName):
    fileName = 'allFile/img/'+fileName

    img.save(fileName)

# 提示区显示信息
def showNoteInf(inf_s):
    global iniC
    iniC.changeNoteInf(inf_s)

def getClassRoomDic():
    with open('allFile/settings.txt','r') as rfile:
        s = rfile.read()
        s_json = json.loads(s)
    return s_json['classRoomDic']

# 开始监听
def startLis():
    # 获取配置信息
    global classRoomDic
    classRoomDic = getClassRoomDic()

    # 打开状态窗口
    global iniC
    iniC = init_class()
    iniC.layout()

    # 开始键鼠监听
    mouseLisT = threading.Thread(target=startMouseLis)
    keyBoardLisT = threading.Thread(target=startKeyboardLis)
    mouseLisT.start()
    keyBoardLisT.start()

# 结束监听
def endLis():

    # 关闭状态窗口
    global iniC
    iniC.destroy()

    # 结束键鼠监听
    mouseListener.stop()
    keyListener.stop()