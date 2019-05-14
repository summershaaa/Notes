# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 12:41:53 2019

@author: WinJX
"""
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style = 'darkgrid')


#对图像做直方图均衡化
def histImageArr(img_arr, cdf):
    '''
    img_arr:灰度图像数组
    cdf:累积分布值，其中cdf[-1]为灰度值总个数，即图宽*图高
    map_list:用于映射变换前后的灰度值
    img_list:存储均衡化后的图像数据
    '''
    #获得灰度值映射表
    map_list = []
    for val in cdf:
        map_list.append(int(255*val/cdf[-1]))
     
    #根据映射表更新图像灰度值
    width,height = img_arr.shape
    for i in range(width):
        for j in range(height):
            img_arr[i,j] = map_list[img_arr[i,j]]
    return img_arr


#对图像做对数变换
def log_transformation(img_arr,c):
    rows,cols = img_arr.shape
    for i in range(rows):
        for j in range(cols):
            img_arr[i][j] = c * np.log(1 + img_arr[i][j])
    return Image.fromarray(np.array(img_arr))


#可视化对比图
def plt_show(img,new_img,img_arr,new_arr,string):
    plt.figure(figsize = (20,14))
    plt.subplot(221)
    plt.imshow(img)
    plt.title('原图',fontproperties = 'SimHei',fontsize = 18)
    plt.axis('off')
    plt.subplot(222)
    plt.imshow(new_img)
    plt.title(string,fontproperties = 'SimHei',fontsize = 18)
    plt.axis('off')
    plt.subplot(223)
    plt.hist(img_arr.ravel(),bins=256,facecolor='blue',alpha =1)
    plt.title('频率直方图',fontproperties = 'SimHei',fontsize = 18)
    plt.xlabel('灰度值',fontproperties = 'SimHei',fontsize = 16)
    plt.ylabel('频数',fontproperties = 'SimHei',fontsize = 16)
    plt.xlim(100,256)
    plt.subplot(224)
    plt.hist(new_arr.ravel(),bins=256)
    plt.title('频率直方图',fontproperties = 'SimHei',fontsize = 18)
    plt.xlabel('灰度值',fontproperties = 'SimHei',fontsize = 16)
    plt.ylabel('频数',fontproperties = 'SimHei',fontsize = 16)
    plt.xlim(-1,256)
    plt.show()

#直方图均衡化
def main1():
    img = Image.open('./montain.jpg')
    img_arr = np.array(img)
    img_copy = img_arr.copy()  #备份原始数据
    #统计图片中各灰度值出现的频数
    img_hist, bins = np.histogram(img_arr.flatten(), range(256))
    #用cumsum()函数计算频数累加和
    cdf = img_hist.cumsum()   #len(cdf) = 255
    new = histImageArr(img_arr,cdf)
    new_arr = np.array(new)
    new_img = Image.fromarray(new_arr)
    string = '直方图均衡化后的图片'
    plt_show(img,new_img,img_copy,new_arr,string)

#对数变换
def main2():
    img = Image.open('./city.jpeg')
    img_arr = np.array(img)
    rows,cols,_ = img_arr.shape   #(413, 649, 3)
    c = 255/np.log(256)           # s = c*log(1+r) 
    r,g,b = img.split()           #分离三通道
    #分别获得三个通道经对数变换的结果
    img_r = log_transformation(np.array(r),c)
    img_g = log_transformation(np.array(g),c)
    img_b = log_transformation(np.array(b),c)
    #合并三通道为彩图
    new_img = Image.merge('RGB',(img_r,img_g,img_b))
    string = '对数变换后的图片'
    plt_show(img,new_img,img_arr,np.array(new_img),string)


if __name__ == '__main__':
    main1()
    main2()


