# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 10:27:14 2019

@author: WinJX
"""

#seaborn可视化(2) —— 分类

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="ticks", color_codes=True)
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 
sns.set(font = 'SimHei')
sns.set(font_scale=1.5)
tips = sns.load_dataset('tips')

"""
sns.catplot(
    ['x=None', 'y=None', 'hue=None', 'data=None', 'row=None', 'col=None',
    'col_wrap=None', 'estimator=<function mean at 0x000001A2D75D2950>',
    'ci=95', 'n_boot=1000', 'units=None', 'order=None', 'hue_order=None', 
    'row_order=None', 'col_order=None', "kind='strip'", 'height=5',
    'aspect=1', 'orient=None', 'color=None', 'palette=None', 'legend=True', 
    'legend_out=True', 'sharex=True', 'sharey=True', 'margin_titles=False',
    'facet_kws=None', '**kwargs'],)
"""

#默认情况
sns.catplot(x="day", y="total_bill", data=tips)

#jitter : 控制数据抖动
sns.catplot(x="day", y="total_bill", jitter=False, data=tips)

"""
第二种方法使用防止重叠的算法沿分类轴调整点。虽然它只适用于相对较小的数据集,
但它可以更好地表示观测值的分布。这种情节有时被称为“beeswarm”，
由swarmplot()在seaborn中绘制，在catplot()中设置kind=“swarm”激活swarmplot()
"""
sns.catplot(x="day", y="total_bill", kind="swarm", data=tips)


#hue : 分组类别
sns.catplot(x="day", y="total_bill", hue="sex", kind="swarm", data=tips)

#筛选数据
sns.catplot(x="size", y="total_bill", kind="swarm",
            data=tips.query("size != 3"))

#指定顺序
sns.catplot(x="smoker", y="tip", order=["No", "Yes"], data=tips)

#轴序
sns.catplot(x="total_bill", y="day", hue="time", kind="swarm", data=tips)


#类别的分布
#箱型图
sns.catplot(x="day", y="total_bill", kind="box", data=tips)

# hue : 类间分类
sns.catplot(x="day", y="total_bill", hue="smoker", kind="box", data=tips)


# 指定分组
tips["weekend"] = tips["day"].isin(["Sat", "Sun"])
sns.catplot(x="day", y="total_bill", hue="weekend",
            kind="box", dodge=False, data=tips)


"""
一个相关的函数boxenplot()绘制了一个类似于箱形图的图，但是经过了优化，
可以显示关于分布形状的更多信息。它最适合较大的数据集:
"""
diamonds = sns.load_dataset("diamonds")
sns.catplot(x="color", y="price", kind="boxen",
            data=diamonds.sort_values("color"))


#小提琴图：结合了箱线图和分布教程中描述的内核密度估计过程
sns.catplot(x="total_bill", y="day", hue="time",
            kind="violin", data=tips)

#分割小提琴
sns.catplot(x="day", y="total_bill", hue="sex",
            kind="violin", split=True, data=tips)

#显示每个单独数据的观察值
sns.catplot(x="day", y="total_bill", hue="sex",
            kind="violin", inner="stick", split=True,
            palette="pastel", data=tips)

#结合散点图和小提琴图
g = sns.catplot(x="day", y="total_bill", kind="violin", inner=None, data=tips)
sns.swarmplot(x="day", y="total_bill", color="k", size=3, data=tips, ax=g.ax)



#类别内统计估计
#barplot:条形图
titanic = sns.load_dataset("titanic")
sns.catplot(x="sex", y="survived", hue="class", kind="bar", data=titanic)

#countplot() :使用条形图显示每个分类库中的观察计数
sns.catplot(x="deck", kind="count", palette="ch:.25", data=titanic)

#计数分组
sns.catplot(y="deck", hue="class", kind="count",
            palette="pastel", edgecolor=".6",
            data=titanic)

#pointplot :使用散点图符号显示点估计和置信区间
sns.catplot(x="sex", y="survived", hue="class", kind="point", data=titanic)