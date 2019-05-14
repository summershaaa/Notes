# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 15:10:10 2018

@author: WinJX
"""
import re
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

'''该函数用于读取文本并断句'''
def read_word(filename):
    with open(filename, 'r') as f2:
        words = f2.read()
    # 将文本分割成句子
    words = re.split(r'[.|?|!]', words)
    # 对句子做清除两边多余符号和转小写处理
    sentence = [x.strip(' .').lower() for x in words]
    sentence_list = []
    for item in sentence:
        # 将每个句子分割成一串单词
        get_sentence = re.split(r"\b[\s\.,();\"]+?\b", item.strip())
        sentence_list.append(get_sentence)  # 添加至列表当中
    return sentence_list      #返回处理好的单词表

'''最长公共子序列函数，返回公共子序列长度矩阵表'''
def lcs(a, b):
    len_a = len(a)
    len_b = len(b)
    matrix_c = [[0 for i in range(len_b + 1)] for j in range(len_a + 1)]  #构造矩阵
    flag=[[0 for i in range(len_b+1)] for j in range(len_a+1)]
    for i in range(len_a):
        for j in range(len_b):  
            if a[i] == b[j]:   #第一种情况,'↖'
                matrix_c[i + 1][j + 1] = matrix_c[i][j] + 1
                flag[i+1][j+1]='ok'
            elif matrix_c[i + 1][j] > matrix_c[i][j + 1]:#第二种情况,'←'
                matrix_c[i + 1][j + 1] = matrix_c[i + 1][j]
                flag[i+1][j+1]='left'
            else:              #第三种情况，'↑'
                matrix_c[i + 1][j + 1] = matrix_c[i][j + 1]
                flag[i+1][j+1]='up'
    return matrix_c,flag

'''计算匹配值'''
def compare(la, lb):
    matrix_c,flag = lcs(la, lb)  
    the_same = max(max(matrix_c))  #得到匹配单词个数
    if len(la) < len(lb):          #la > lb
        the_space = 0
        the_error = len(lb) - len(la)
    else:                          #la < lb
        the_space = len(la) - len(lb)
        the_error = len(lb) - the_same
    #返回匹配值
    return (the_same - the_space * 0.5 - the_error) / len(la)

'''插空'''
def align(l1,l2):
    l1 = list(l1)
    l2 = list(l2)
    i = len(l1)
    j = len(l2)
    matrix_c,flag = lcs(l1,l2)
    while flag[i][j] != 0:
        if flag[i][j] == 'ok':
            i -= 1
            j -= 1
        elif flag[i][j] == 'left':
            l1.insert(i,'-')
            j -= 1
        elif flag[i][j] == 'up':
            l2.insert(j,'-')
            i -= 1
    return l1,l2

'''对齐打印输出'''
def map_output(max_map):
    for cnt, (i, j) in enumerate(max_map):
        l,r = align(rst_text[i],rst_lib[j])
        print("{0}text中第{1}句,lib中第{2}句,重复率：{3:.2f}{0}".format(
                '-' * 60, i + 1, j + 1, time_rate[cnt][-1]))
        for word in l:
            print('{:<16}'.format(word),end = '    ')
        print('\n')
        for word in r:
            print('{:<16}'.format(word),end = '    ')
        print('\n')
    return ''

'''主函数'''
if __name__ == '__main__':
    path_text = r'./text2.txt'  # text2.txt文本的路径
    path_lib = r'./lib.txt'  # lib.txt文本的路径
    # 将路径作为参数传入函数中即可得到sentence_list
    rst_text = read_word(path_text)[:-1]
    rst_lib = read_word(path_lib)[:-1]
    time_rate = []    #存放着(match,rate)-->(匹配单词个数,相似度)
    max_map = []      #存放着(0,3)-->代表text的第0句与lib的第3句相似度最高
    rate_line = []    #存放text每个句子的最高匹配度值
    
    for text in rst_text:
        tempmax = 0   #初始化匹配值最高值
        index_lib = 0 #初始化lib的索引
        for lib in rst_lib:
            #调用compare()函数得到匹配值
            temp = compare(text, lib)
            if temp > tempmax:  #比较，若大于上一次的匹配值，则更新匹配值
                tempmax = temp  
                index_lib = rst_lib.index(lib)   #记录lib的索引
        rate_line.append(tempmax)   
        if tempmax >= 0.4:   #若最高匹配值大于0.4则认为重复
            index_text = rst_text.index(text)    #记录此时的text索引
            time_rate.append((len(text), tempmax))  #记录相应信息
            max_map.append((index_text, index_lib)) #记录相应信息
            
    print('匹配个数'+'    '+'匹配值')
    for i,j in time_rate:
        print('   {0}  ---  {1:.2f}'.format(i,j))
    print('text的第m个句子'+'     '+'lib的第n个句子')
    for i,j in max_map[:8]:
        print('    0{0:>}  ---------------  {1:>}'.format(i,j))
    for i,j in max_map[8:]:
        print('    {0:>}  ---------------  {1:>}'.format(i,j))
        
    sum_value = 0    #初始化重复单词个数
    for len_i, rate_i in time_rate:
        sum_value += (len_i * rate_i)       #得到重复句子单词个数
    total = sum([len(x) for x in rst_text]) #得到text中总单词个数
    #输出结果
    print('text文本与lib文本的相似度:{0:.2f}'.format( sum_value / total))
    print(map_output(max_map))
    #可视化相似度折线图
    plt.plot(rate_line,'-ob')
    plt.xlabel('text中的句子',fontproperties="SimHei",fontsize = 16)
    plt.ylabel('在lib中的相似度',fontproperties="SimHei",fontsize = 15) 
    y = [0.4]*12
    plt.plot(y,'--k')
    plt.show()
    


























'''
if __name__ == '__main__':
    path_text = r'./text2.txt'  # text2.txt文本的路径
    path_lib = r'./lib.txt'  # lib.txt文本的路径
    # 将路径作为参数传入函数中即可得到sentence_list
    rst_text = read_word(path_text)[:-1]
    rst_lib = read_word(path_lib)[:-1]
    dict = {}
    for text in rst_text:
        tempmax = 0
        for lib in rst_lib:
            temp = compare(text, lib)
            if temp > tempmax:
                tempmax = temp
        if tempmax >= 0.4:
            dict[len(text)] = tempmax
# print(len(dict))
    print(dict)
    list_dict = list(zip(dict.keys(), dict.values()))
# print(list_dict)
    sum_value = 0
    for len_i, rate_i in list_dict:
        sum_value += (len_i * rate_i)
# print(sum_value)
    total = sum([len(x) for x in rst_text])
    print(total)
# print(total)
    print(sum_value / total)

# print(rst_lib)
# print(len(rst_lib[0]))
    # print(len(rst_text[0]))
    print(rst_text[3])
    print(rst_lib[8])
'''