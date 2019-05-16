# -*- coding: utf-8 -*-
"""
Created on Tue May 14 14:25:26 2019

@author: WinJX
"""

import numpy as np
import copy
class Box_Smoothing:
    def __init__(self,data,depth,threshold):
        self.data = data            #未分箱数据 
        self.depth = depth          #箱子深度
        self.threshold = threshold  #离群点阈值
        
    #该函数将原始数据进行分箱
    def Bins(self):
        length = len(self.data)  #数据的个数
        #算出箱子的个数
        if length%self.depth == 0:
            bins = length//self.depth
        else:
            bins = length//self.depth + 1
        #可能最后一个箱子数据不够，所以需要填充数据
        diff = bins*self.depth - length
        #填充若干个数据
        if diff > 0:
            for i in range(diff):
                data.append(data[-1])
            
        #构造分箱后的数组,维度为：(箱数，箱深) 
        array = np.array(self.data).reshape(bins,self.depth)
        #返回分箱后的结果
        return array
    
    #法一：按均值平滑，并返回离群点
    def Smoothing_By_Mean(self):
        #得到分箱后的数据
        array = self.Bins()
        #计算每行(每个箱子)的均值，并四舍五入
        row_mean = array.mean(axis=1)+0.5
        row_mean = [int(x) for x in row_mean]
        #进行均值平滑
        for i in range(self.depth):
            array[:,i] = row_mean
            
        print('----------按均值平滑法-----------')
        print(array)
        
    #法二：按中位数平滑
    def Smoothing_By_Median(self):
        #得到分箱后的数据
        array = self.Bins()
        #深拷贝原数组
        copy_array = copy.deepcopy(array)
        #得到每行(每个箱子)的中位数，并四舍五入
        row_median = np.median(array,axis=1)+0.5
        row_median = [int(x) for x in row_median]
        #进行中位数平滑
        for i in range(self.depth):
            array[:,i] = row_median
        print('----------按中位数平滑法---------')
        print(array)
        #计算平滑后数组与原数组的绝对差值
        diff = abs(array - copy_array)
        #如果差值大于等于10，则为离群点
        outlier = copy_array[diff>=self.threshold]
        #存在离群点则打印出来
        if outlier.size > 0:
            print('离群点为:' ,outlier)
            

    #法三：按边界值平滑
    def Smoothing_By_Boundary(self):
        #得到分箱后的数据
        array = self.Bins()
        #左右边界值
        left,right = array[:,0],array[:,-1]
        #需要平滑的列数
        diff = self.depth - 2
        #进行按边界值平滑，平滑差值小的边界值，如果左右边界差值相等，默认选择左边界值
        for col in range(1,diff+1):
            t = array[:,col]          #取出当前列 
            diff_left = abs(t-left)   #当前列与左边界的绝对差值
            diff_right = abs(t-right) #当前列与右边界的绝对差值
            #标记，如果当前列与左边界的差值 <= 当前列与右边界的差值，则标记为1，否则标记为0 
            flag = np.where(diff_left <= diff_right,1,0)
            #对当前列的每一个元素进行边界平滑
            for idx in range(len(t)):
                #如果当前索引下标记为1，则向左边界值平滑，否则向右边界值平滑
                t[idx] = left[idx] if flag[idx] == 1 else right[idx]
        #因为是原地操作，所以直接返回原数组即可
        print('----------按边界值平滑法---------')
        print(array)    
        
    #法四：按中列数平滑
    def Smoothing_By_Midran(self):
        #得到分箱后的数据
        array = self.Bins()
        #计算每行(每个箱子)的中列数，并四舍五入
        row_midran = (array[:,0]+array[:,-1])/2+0.5
        row_midran = [int(x) for x in row_midran]
        #进行均值平滑
        for i in range(self.depth):
            array[:,i] = row_midran
            
        print('----------按中列数平滑法---------')
        print(array)
    
if __name__ == '__main__':
#data = [13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 
#        30, 33, 33, 35, 35, 35, 35, 36, 40, 45, 46, 52, 70]

    data = np.loadtxt('./data.txt')
    #为防止数据格式问题，统一把数据转化成列表形式
    data = list(data)
    print("请输入箱的深度({0}-{1})".format(1,len(data)))
    depth = int(input())
    if depth < 1 or depth > len(data):
        raise ValueError("请输入有效整数")
    threshold = 10   #设置离群点阈值
    rst = Box_Smoothing(data,depth,threshold)
    print('--------分箱后未平滑的数据--------')
    print(rst.Bins())
    #按均值平滑，并输出离群点
    rst.Smoothing_By_Mean()
    print('--------------------------------')
    #按中位数平滑
    rst.Smoothing_By_Median()
    print('--------------------------------')
    #按边界值平滑
    rst.Smoothing_By_Boundary()
    print('--------------------------------')
    #按中列数平滑
    rst.Smoothing_By_Midran()

    
 """
    请输入箱的深度(1-27)
3
--------分箱后未平滑的数据--------
[[13. 15. 16.]
 [16. 19. 20.]
 [20. 21. 22.]
 [22. 25. 25.]
 [25. 25. 30.]
 [33. 33. 35.]
 [35. 35. 35.]
 [36. 40. 45.]
 [46. 52. 70.]]
----------按均值平滑法-----------
[[15. 15. 15.]
 [18. 18. 18.]
 [21. 21. 21.]
 [24. 24. 24.]
 [27. 27. 27.]
 [34. 34. 34.]
 [35. 35. 35.]
 [40. 40. 40.]
 [56. 56. 56.]]
--------------------------------
----------按中位数平滑法---------
[[15. 15. 15.]
 [19. 19. 19.]
 [21. 21. 21.]
 [25. 25. 25.]
 [25. 25. 25.]
 [33. 33. 33.]
 [35. 35. 35.]
 [40. 40. 40.]
 [52. 52. 52.]]
离群点为: [70.]
--------------------------------
----------按边界值平滑法---------
[[13. 16. 16.]
 [16. 20. 20.]
 [20. 20. 22.]
 [22. 25. 25.]
 [25. 25. 30.]
 [33. 33. 35.]
 [35. 35. 35.]
 [36. 36. 45.]
 [46. 46. 70.]]
--------------------------------
----------按中列数平滑法---------
[[15. 15. 15.]
 [18. 18. 18.]
 [21. 21. 21.]
 [24. 24. 24.]
 [28. 28. 28.]
 [34. 34. 34.]
 [35. 35. 35.]
 [41. 41. 41.]
 [58. 58. 58.]]
    """
    
    
    
