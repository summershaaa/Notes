# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:03:32 2019

@author: WinJX
"""

from PIL import Image
from PIL import ImageChops
import cv2
import numpy as np
import matplotlib.pyplot as plt

#rotate
def rotate(im1,im2,angle,width,height):
    """
    im1:使用PIL读取的图片
    im2:使用cv2读取的图片
    angle:旋转角度
    width:图片宽度
    height:图片高度
    """
    
    #使用PIL库的rotate函数旋转
    pil_rotated = im1.rotate(angle)  
    #先通过getRotationMatrix2D函数得到图像的旋转矩阵
    temp = cv2.getRotationMatrix2D((width//2,height//2),angle,1)  
    #再通过仿射变换函数warpAffine得到旋转后的图像
    cv_rotate = cv2.warpAffine(im2,temp,(width,height))
    #将opencv中的BGR格式转换成RGB格式，方便后续使用matplotlib正常显示图片
    cv_rotated = cv2.cvtColor(cv_rotate,cv2.COLOR_BGR2RGB)
    #返回两种方法得到的结果
    return pil_rotated,cv_rotated


#scale
def scale(im1,im2,scale_ratio,width,height):
    """
    scale_ratio:缩放比例
    Image.ANTIALIAS:抗锯齿
    """ 
    
    pil_scaled = im1.resize((width//scale_ratio[0],height//scale_ratio[1]),Image.ANTIALIAS)
    cv_scale = cv2.resize(im2,(width//scale_ratio[0],height//scale_ratio[1])) 
    cv_scaled = cv2.cvtColor(cv_scale,cv2.COLOR_BGR2RGB)
    return pil_scaled,cv_scaled


#shift
def shift(im1,im2,shift_size,width,height):
    """
    M:自定义平移矩阵
    """
    
    pil_shifted = ImageChops.offset(im1,width//shift_size[0],height//shift_size[1])
    M = np.float32([[1,0,width//shift_size[0]],[0,1,height//shift_size[1]]])
    cv_shift = cv2.warpAffine(im2,M,(width,height))
    cv_shifted = cv2.cvtColor(cv_shift,cv2.COLOR_BGR2RGB)
    return pil_shifted,cv_shifted


#可视化对比结果图
def plt_show(image,title_name):
    plt.figure(figsize = (20,8))
    plt.subplot(121)
    plt.imshow(image[0])
    plt.title(title_name[0],fontproperties = 'SimHei',fontsize = 20)
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(image[1])
    plt.title(title_name[1],fontproperties = 'SimHei',fontsize = 20)  
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    pil_read = Image.open('./gulfstream.png')    #使用PIL读取图片
    cv_read = cv2.imread('./gulfstream.png')     #使用cv2读取图片
    width,height = pil_read.size                 #获取图片的宽高
    #设置变换因子
    angle,scale_ratio,shift_size = [45,[3,5],[8,6]]
    #格式化输出
    fmt1 = '逆时针旋转{0}°'.format(angle)
    fmt2 = '沿X轴缩放1/{0},Y轴缩放1/{1}'.format(str(scale_ratio[0]),str(scale_ratio[1]))
    fmt3 = '沿X轴平移1/{0},Y轴平移1/{1}'.format(str(shift_size[0]),str(shift_size[1]))
    
    #原图输出
    plt.figure(figsize = (9,8))
    plt.imshow(pil_read)
    plt.title('原图',fontproperties = 'SimHei',fontsize = 20)
    plt.axis('off')
    #图片旋转
    rotated_image = rotate(pil_read,cv_read,angle,width,height)
    plt_show(rotated_image,['PIL'+fmt1,'cv2'+fmt1])
    #图片缩放
    scaled_image = scale(pil_read,cv_read,scale_ratio,width,height)
    plt_show(scaled_image,['PIL'+fmt2,'cv2'+fmt2])
    #图片平移
    shifted_image = shift(pil_read,cv_read,shift_size,width,height)
    plt_show(shifted_image,['PIL'+fmt3,'cv2'+fmt3])


    