# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 14:18:32 2018

@author: WinJX
"""
import re


def Merge_Sort(list_a):  # 归并排序
    if len(list_a) <= 1:  # 判断列表元素个数,若为一个直接返回列表
        return list_a
    else:
        mid = len(list_a) // 2  # 取中点
        list_l = Merge_Sort(list_a[:mid])  # 切片得到左半部分
        list_r = Merge_Sort(list_a[mid:])  # 切片得到右半部分

    return Merge(list_l, list_r)  # 合并左右两部分


def Merge(list_l, list_r):  # 合并函数
    left, right = 0, 0  # 初始化起点
    rst = []  # 储存结果
    while left < len(list_l) and right < len(list_r):  # 循环条件
        if list_l[left] < list_r[right]:  # 比较，取小的那个
            rst.append(list_l[left])
            left += 1
        else:
            rst.append(list_r[right])
            right += 1

    rst += list_l[left:]  # 合并排好序的左半部分
    rst += list_r[right:]  # 合并排好序的右半部分
    return rst  # 返回得到的结果


if __name__ == '__main__':
    with open(r'./text.txt', 'r') as f:
        str = f.read()      # 读取文本
    str = str.rstrip('.')   # 去除最右边的'.'
    all_words = re.split(r"\b[\s\.,();\"]+?\b", str)   # 正则分割
    word_list = [x.lower() for x in all_words]         # 首字母全部转小写
    dict_word = {}          # 构造一个字典，键存放单词，值存放出现次数
    for word in word_list:  # 遍历单词表
        if word not in dict_word.keys():  # 第一次出现，赋初值1
            dict_word[word] = 1
        else:                             # 该单词出现次数加1
            dict_word[word] += 1
    list_1 = zip(dict_word.keys(), dict_word.values())  # 将字典构造成元组形式存放在列表中
    list_a = [x for x in list_1]          # 得到[('in',9),('and',12)...]形式的列表,用于按字母排序
    list_2 = zip(dict_word.values(), dict_word.keys())
    list_b = [x for x in list_2]         # 得到[(9,'in'),(12,'and')...]形式的列表,用于按词频排序
    rst1 = Merge_Sort(list_a)
    print('     按字母排序')
    for k, v in rst1:
        print('{0:<15} {1:>4}'.format(k, v))
    print('')
    rst1 = Merge_Sort(list_b)
    print('     按频率排序')
    for k, v in rst1[::-1]:
        print('{0:<15} {1:>4}'.format(v, k))