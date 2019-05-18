# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 21:07:04 2018

@author: WinJX
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import pairwise_distances_argmin

def k_means(data,k):
    #设置随机数种子
    rng = np.random.RandomState(3)
    #随机挑选k个值
    i = rng.permutation(data.shape[0])[:k]
    #随机选择的k个中心点
    center = data[i]
    while True:
        #根据离中心点距离来选择簇
        labels = pairwise_distances_argmin(data,center)
        #更新中心点
        new_center = np.array([data[labels == i].mean(0) for i in range(k)])
        #如果中心点未发生变化，则退出循环
        if np.all(center == new_center):
            break
        #否则更新中心点
        center = new_center
    #返回中心点坐标和数据簇类标签
    return center,labels


if __name__ == '__main__':
    #读取数据，第一行为数据信息
    data = np.loadtxt('./data.txt')
    #获取簇个数
    k = data[:1,:1]
    #数据大小
    datasize = data[:1,:-1]
    #实验数据
    data = data[1:,:]
    #调用聚类算法得到中心点和标签
    center,labels = k_means(data,3)
    #输出中心点坐标和该簇数据
    for k,num in enumerate(center,1):
        print('------------------------------------------------------')
        print('第{}个簇中心点坐标:{}'.format(k,center[k-1,:]))
        print('在该簇中的数据:')
        print(data[labels==k-1])

    #可视化
    fig = plt.figure()
    axes3d = Axes3D(fig)
    axes3d.scatter(data[:,0],data[:,1],data[:,2],c = labels,cmap = 'viridis',s= 40)
    axes3d.scatter(center[:,0],center[:,1],center[:,2],c='red',s = 100)
    plt.show()
