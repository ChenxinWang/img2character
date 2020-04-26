# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 20:05:10 2020

@author: Now
"""
from PIL import Image
import cv2

#PIL的写法
def img2charsPIL(img_path, scale, chars):
    img = Image.open(img_path).convert("L")
    
    chars_len = len(chars)
    out_str = ''
    width, height = img.size
    
    if width > scale:
        height = int(height * scale / width / 2)
        width = scale
    img = img.resize((width, height), Image.ANTIALIAS)
    
    #灰度图像素值0-255映射到chars上,本例中为每隔256 / 8 = 32个像素是一类字符
    for i in range(height):
        for j in range(width):
            pixel = img.getpixel((j, i))
            out_str += chars[int(chars_len * pixel / 256 ) - 1]
        out_str += '\r\n'
    return out_str

#OpenCV的写法
def img2charsCV(imgPath, scale, chars):
    img = cv2.imread(imgPath, 0)
        
    chars_len = len(chars)
    out_str = ""
    
    #interpolation : INTER_NEAREST INTER_LINEAR INTER_AREA INTER_CUBIC INTER_LANCZOS4
    #interpolation=cv2.INTER_AREA效果更接近Image.ANTIALIAS
    img = cv2.resize(img, (scale, int(img.shape[0] * scale / img.shape[1] / 2)), interpolation=cv2.INTER_LANCZOS4)
    
    h = img.shape[0]
    w = img.shape[1]
    #灰度图像素值0-255映射到chars上,本例中为每隔256 / 8 = 32个像素是一类字符
    for i in range(h):
        for j in range(w):
            gray = img[i][j]
            out_str += chars[int(chars_len * gray / 256 ) - 1]
        out_str += "\r\n"
    return out_str

if __name__ == "__main__":
    #\033[33m{}\033[0m形成黄色字符,033[36m{}\033[0m形成蓝色字符
    #chars = ['.', '\033[33m?\033[0m', '@', '#', '\033[36m¿\033[0m', '*', '$', '\'']
    chars = ['\'', '\033[36m¿\033[0m', '\033[36m¿\033[0m', '*', '\033[33m?\033[0m', '\033[33m?\033[0m', '.', '@']
    print(img2charsPIL('1.jpg', 150, chars))
    print(img2charsCV('1.jpg', 150, chars))
