# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 19:50:35 2019

@author: WinJX
"""

import matplotlib.pyplot as plt
from PIL import Image  
from skimage.filters import roberts,prewitt
import cv2

def plt_show(img,new_img,img_arr,new_arr,string = ['canny','sobel','laplacian','prewitt']):
    plt.figure(figsize = (14,8))
    plt.subplot(221)
    plt.imshow(img)
    plt.title(string[0],fontproperties = 'SimHei',fontsize = 18)
    plt.axis('off')
    plt.subplot(222)
    plt.imshow(new_img)
    plt.title(string[1],fontproperties = 'SimHei',fontsize = 18)
    plt.axis('off')
    plt.subplot(223)
    plt.imshow(img_arr)
    plt.title(string[2],fontproperties = 'SimHei',fontsize = 18)
    plt.axis('off')
    plt.subplot(224)
    plt.imshow(new_arr)
    plt.title(string[3],fontproperties = 'SimHei',fontsize = 18)
    plt.axis('off')
#    plt.subplot(235)
#    plt.imshow(img5)
#    plt.title(string[4],fontproperties = 'SimHei',fontsize = 18)
#    plt.axis('off')
#    plt.subplot(236)
#    plt.imshow(img6)
#    plt.title(string[5],fontproperties = 'SimHei',fontsize = 18)
#    plt.axis('off')
    
    plt.show()
 

#img1 = Image.open('lena.jpg')
#img2 = Image.open('sobel_x_lena.jpg')
#img3 = Image.open('sobel_y_lena.jpg')
#img4 = Image.open('sobel_xy_lena.jpg')
#plt_show(img1,img2,img3,img4)


image=cv2.imread('./lena.jpg',cv2.IMREAD_GRAYSCALE)
canny = cv2.Canny(image,100,200)
sobel = cv2.Sobel(image,cv2.CV_8U, 1 , 1)
laplacian = cv2.Laplacian(image, -1)
prewitt = prewitt(image)

plt_show(canny,sobel,laplacian,prewitt)

#gx = cv2.Scharr(image, ddepth=cv2.CV_16S, dx=1, dy=0)
#gy = cv2.Scharr(image, ddepth=cv2.CV_16S, dx=0, dy=1)
#gx_abs = cv2.convertScaleAbs(gx)
#gy_abs = cv2.convertScaleAbs(gy)
#scharr = cv2.addWeighted(src1=gx_abs, alpha=0.5, src2=gy_abs, beta=0.5, gamma=0)
#
#
#
#
#
#laplacian = cv2.Laplacian(image, -1)
#
#robert = roberts(image)

