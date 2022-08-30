from PIL import Image
import matplotlib.pyplot as plt
import cv2
from imgTool.typeTransform import pil2cv
# from typeTransform import pil2cv
import pyautogui
import aircv as ac                  # 图像识别
from paddleocr import PaddleOCR     # 文字识别

def imgCut(img, left, upper, right, lower):
    """
        原图与所截区域相比较
    :param img: 图片
    :param left: 区块左上角位置的像素点离图片左边界的距离
    :param upper：区块左上角位置的像素点离图片上边界的距离
    :param right：区块右下角位置的像素点离图片左边界的距离
    :param lower：区块右下角位置的像素点离图片上边界的距离
     故需满足：lower > upper、right > left
    """

    box = (left, upper, right, lower)
    roi = img.crop(box)

    return roi


# def imgSearch(target,template):
#     target = pil2cv(target)
#     template = pil2cv(template)
#
#
#     result = cv2.matchTemplate(target,template,4)
#
#     min_max = cv2.minMaxLoc(result)
#
#     match_loc = min_max[3]
#
#     return match_loc

def imgSearch(target,template):
    target = pil2cv(target)
    template = pil2cv(template)

    target = pil2cv(target)
    template = pil2cv(template)

    ansImg = ac.find_template(target,template,threshold=0.9)

    return ansImg


def screenShoot():
    im = pyautogui.screenshot()

    return im

def showImg(im):
    plt.imshow(im)

    plt.show()

def wordReg(filePath):
    ans = ''

    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    # 输入待识别图片路径
    img_path = filePath
    # 输出结果保存路径
    result = ocr.ocr(img_path, cls=True)
    for line in result:
        ans += line[-1][0]

    return ans


# target = Image.open("../img/1.png")
# template = Image.open("../img/112.jpg")
#
# ans = imgSearch(target,template)
#
# print(ans)
#
#
# img1 = imgCut(target,ans[0][0],ans[0][1],ans[3][0],ans[3][1])
#
# plt.imshow(img1)
#
# plt.show()