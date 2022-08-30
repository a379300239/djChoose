import cv2
import numpy
from PIL import Image


def pil2cv(image):
    image = cv2.cvtColor(numpy.asarray(image),cv2.COLOR_RGB2BGR)
    return image

def cv2pil(image):
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    return image