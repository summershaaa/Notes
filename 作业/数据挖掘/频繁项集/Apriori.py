# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:06:56 2019

@author: WinJX
"""

import itertools
import collections
#连接步，连接k-1项集为k项集
def join_step(itemsets):
    """
    itemsets:所有项集，list(tuple)格式 
    """
    i = 0
    while i < len(itemsets):
        skip = 1
        #对每个项集进行解序列，因为满足最后一个元素之前的元素都相同时才进行连接
        *itemset_first, itemset_last = itemsets[i]
        tail_items = [itemset_last]
        tail_items_append = tail_items.append  
        #选择可以连接的其他项集
        for j in range(i + 1, len(itemsets)):
            *itemset_n_first, itemset_n_last = itemsets[j]
            #满足连接条件，进行连接
            if itemset_first == itemset_n_first:
                tail_items_append(itemset_n_last)
                skip += 1
            #不满足连接条件，跳出当前循环
            else:
                break
        #当前连接工作已完成
        itemset_first = tuple(itemset_first)
        #生成候选项集
        for a, b in sorted(itertools.combinations(tail_items, 2)):
            yield itemset_first + (a,) + (b,)
        i += skip

#剪枝步
def prune_step(itemsets, possible_itemsets):
    """
    itemsets:k项集，list(tuple)格式 
    possible_itemsets:候选k+1项集
    剪枝原理：所有频繁项集的非空子集也一定是频繁的
    """
    
    itemsets = set(itemsets)
    for possible_itemset in possible_itemsets:

        for i in range(len(possible_itemset) - 2):
            removed = possible_itemset[:i] + possible_itemset[i + 1 :]
            #子集不是频繁项集，直接剪枝掉
            if removed not in itemsets:
                break
        #所有子集都是频繁的，所以保留下来
        else:
            yield possible_itemset


def apriori_gen(itemsets):
    #生成所有频繁k项集
    possible_extensions = join_step(itemsets)
    #生成候选k+1项集
    yield from prune_step(itemsets, possible_extensions)


def itemsets_from_transactions(transactions,min_support,max_length,verbosity=0):
    """
    transactions:事务数据
    min_support:最小支持度
    max_length:事务中的最大元素个数
    verbosity:打印输出的层数,(0，1，2)
    """
    
    #把事务数据集转化为集合形式
    transaction_sets = [set(t) for t in transactions if len(t) > 0]
    def transactions():
        return transaction_sets
    #定义一个默认字典
    use_transaction = collections.defaultdict(lambda: True)

    #如果打印层级大于0，则输出挖掘信息
    if verbosity > 0:
        print("--------------------挖掘1项集--------------------")
    #定义一个int类型的默认字典，用于统计项集的出现次数
    counts = collections.defaultdict(int)
    #事务数据数量
    num_transactions = 0
    #对所有项集进行计数
    for transaction in transactions():
        num_transactions += 1  
        for item in transaction:
            counts[item] += 1  
    #项集计数信息
    large_itemsets = [(i, c) for (i, c) in counts.items() 
                             if (c / num_transactions) >= min_support]
    #打印1项集个数
    if verbosity > 0:
        num_cand, num_itemsets = len(counts.items()), len(large_itemsets)
        print("找到{}个候选1项集".format(num_cand))
        print("其中有{}个是频繁的".format(num_itemsets))
    #打印所有的频繁1项集
    if verbosity > 1:
        print("{}".format(list((i,) for (i, c) in large_itemsets)))
        print()
    #存储频繁1项集信息
    if large_itemsets:
        large_itemsets = {1: {(i,): c for (i, c) in sorted(large_itemsets)}}
    else:
        return dict(), num_transactions
    #子集
    issubset = set.issubset
    #开始查找频繁k(k>1)项集
    k = 2
    #如果频繁k-1项集存在且最大项集元素个数不为1，则可以继续挖掘k项集
    while large_itemsets[k - 1] and (max_length != 1):
        if verbosity > 0:
            print("--------------------挖掘{}项集--------------------".format(k))
        itemsets_list = list(large_itemsets[k - 1].keys())
        #候选k+1项集
        C_k = list(apriori_gen(itemsets_list))
        #候选k项集里的所有项集
        C_k_sets = [set(itemset) for itemset in C_k]
        #打印输出相关信息
        if verbosity > 0:
            print("找到{}个候选{}项集".format(len(C_k), k))
        #打印候选项集
        if verbosity > 1:
            print("{}".format(C_k))
        if not C_k:
            break
        #查找频繁的k+1项集
        candidate_itemset_counts = collections.defaultdict(int)
        for row, transaction in enumerate(transactions()):
            #子集非频繁，跳过
            if not use_transaction[row]:
                continue
            #标记
            found_any = False
            for candidate, candidate_set in zip(C_k, C_k_sets):
                if issubset(candidate_set, transaction):
                    candidate_itemset_counts[candidate] += 1
                    found_any = True
            #该项集是非频繁的
            if not found_any:
                use_transaction[row] = False
        #记录频繁项集信息
        C_k = [(i, c) for (i, c) in candidate_itemset_counts.items()
                      if (c / num_transactions) >= min_support]
        if not C_k:
            break
        large_itemsets[k] = {i: c for (i, c) in sorted(C_k)}

        if verbosity > 0:
            num_found = len(large_itemsets[k])
            fmt = "其中有{}个是频繁的".format(num_found)
            print(fmt)
        #打印频繁项集
        if verbosity > 1:
            print("{}".format(list(large_itemsets[k].keys())))
        print()
        k += 1
        #超过事务最大元素长度，直接退出
        if k > max_length:
            break
    print()
    print('输出各频繁项集的支持度')
    for key in large_itemsets:
        print('---------频繁{}项集---------'.format(key))
        for k,v in large_itemsets[key].items():
            print('{} : {:.2f} ({}/{})'.format(k,v/9,v,9))
    return ' '


if __name__ == "__main__":
    #读取数据文件
    with open('./data.txt') as f:
        data = f.read()
    #对数据进行清洗，去除多余信息
    data = data.split('\n')
    transactions = [tuple(x.split()) for x in data]
    #最大事务元素个数
    max_length = max(len(tran) for tran in transactions)
    #最小支持度
    min_support = 0.2
    itemsets_from_transactions(transactions,min_support,max_length,2)
    
    