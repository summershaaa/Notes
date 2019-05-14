### -*- coding: utf-8 -*-
##"""
##Created on Wed Apr  3 10:15:27 2019
##
##@author: WinJX
##"""


import cv2
import numpy as np

# 卷积函数
def imgConvolve(image_array, suanzi):
    '''
    :param image: 图片矩阵
    :param saunzi: 检测算子
    :return:卷积后的矩阵
    '''
    image = image_array.copy()     # 原图像矩阵的深拷贝    
    dim1,dim2 = image.shape
    # 对每个元素与算子进行乘积再求和(忽略最外圈边框像素)
    for i in range(1,dim1-1):
        for j in range(1,dim2-1):
            image[i,j] = int((image_array[(i-1):(i+2),(j-1):(j+2)]*suanzi).sum())  
    # 由于卷积后灰度值不一定在0-255之间，统一化成0-255
    image = image*(255.0/image.max())
    # 返回结果矩阵
    return image


# Sobel Edge
def sobelEdge(image, sobel):
    '''
    :param image: 图片矩阵
    :param sobel: 滤波窗口
    :return:Sobel处理后的矩阵
    '''
    return imgConvolve(image, sobel)


# Prewitt Edge
def prewittEdge(image, prewitt):
    '''
    :param image: 图片矩阵
    :param prewitt: 竖直方向
    :return:处理后的矩阵
    '''
    return imgConvolve(image, prewitt)


# sobel 算子
sobel_1 = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

sobel_2 = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]])
# prewitt 算子
prewitt_1 = 1/3*np.array([[-1, 0, 1],
                      [-1, 0, 1],
                      [-1, 0, 1]])

prewitt_2 = 1/3*np.array([[-1, -1, -1],
                      [0, 0, 0],
                      [1, 1, 1]])


#Sobel
image=cv2.imread('lena.jpg',cv2.IMREAD_GRAYSCALE)
img_spbel1 = sobelEdge(image, sobel_1)
cv2.imwrite('sobel_x_lena.jpg',img_spbel1)
img_spbel2 = sobelEdge(image, sobel_2)
cv2.imwrite('sobel_y_lena.jpg',img_spbel2)
image_xy = np.sqrt(img_spbel1**2+img_spbel2**2)
# 梯度矩阵统一到0-255
image_xy = (255.0/image_xy.max())*image_xy
cv2.imwrite('sobel_xy_lena.jpg',image_xy)

#Prewitt
img_prewitt1 = prewittEdge(image, prewitt_1)
cv2.imwrite('prewitt_x_lena.jpg',img_prewitt1)
img_prewitt2 = prewittEdge(image, prewitt_2)
cv2.imwrite('prewitt_y_lena.jpg',img_prewitt2)
image_xy = np.sqrt(img_prewitt1**2+img_prewitt2**2)
# 梯度矩阵统一到0-255
image_xy = (255.0/image_xy.max())*image_xy
cv2.imwrite('prewitt_xy_lena.jpg',image_xy)
