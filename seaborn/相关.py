# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 19:04:31 2019

@author: WinJX
"""

#seaborn可视化(1) —— 相关

#散点图
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 
sns.set(font = 'SimHei')
sns.set(font_scale=1.5)
tips = sns.load_dataset('tips')


"""
sns.scatterplot(
    ['x=None', 'y=None', 'hue=None', 'style=None', 'size=None', 
    'data=None', 'palette=None', 'hue_order=None', 'hue_norm=None',
    'sizes=None', 'size_order=None', 'size_norm=None', 'markers=True',
    'style_order=None', 'x_bins=None', 'y_bins=None', 'units=None', 
    'estimator=None', 'ci=95', 'n_boot=1000', "alpha='auto'", 
    'x_jitter=None', 'y_jitter=None', "legend='brief'", 
    'ax=None', '**kwargs'],)
"""


#默认状态
sns.scatterplot(x = 'total_bill',y = 'tip',data = tips)
sns.relplot(x="total_bill", y="tip", data=tips)

#hue:分组变量
sns.relplot(x = 'total_bill',y = 'tip',hue = 'sex',data = tips)

#hue为数值型的情况
sns.relplot(x="total_bill", y="tip", hue="size", data=tips)

#style : 为每个类使用不同的标记样式
sns.relplot(x = 'total_bill',y = 'tip',hue = 'smoker',style = 'smoker',data = tips)

#size : 设置点的大小
sns.relplot(x="total_bill", y="tip", size="size", data=tips)

#sizes : 设置点大小的范围 
sns.relplot(x="total_bill", y="tip", size="size", sizes=(15, 200), data=tips)


cmap = sns.cubehelix_palette(dark=.3, light=.8, as_cmap=True)
sns.scatterplot(x="total_bill", y="tip",
                hue="size", size="size",
                sizes=(20, 200), palette=cmap,
                legend="full", data=tips)

cmap = sns.cubehelix_palette(dark=.3, light=.8, as_cmap=True)
sns.scatterplot(x="total_bill", y="tip",
                hue="day", size="smoker",
                palette="Set2",
                data=tips)


"""
sns.lineplot(
    ['x=None', 'y=None', 'hue=None', 'size=None', 'style=None', 
     'data=None', 'palette=None', 'hue_order=None', 'hue_norm=None', 
     'sizes=None', 'size_order=None', 'size_norm=None', 'dashes=True',
     'markers=None', 'style_order=None', 'units=None', "estimator='mean'", 
     'ci=95', 'n_boot=1000', 'sort=True', "err_style='band'", 'err_kws=None',
     "legend='brief'", 'ax=None', '**kwargs'],)
"""
#模拟数据
df = pd.DataFrame(dict(time=np.arange(500),
                       value=np.random.randn(500).cumsum()))
g = sns.relplot(x="time", y="value", kind="line", data=df)

"""
更复杂的数据集将对相同的x变量值有多个测量值。
seaborn中的默认行为是通过绘制平均值和平均值周围的95%置信区间
来聚合每个x值的多个度量值
"""
fmri = sns.load_dataset("fmri")
sns.relplot(x="timepoint", y="signal", kind="line", data=fmri)


"""
ci = None
置信区间是使用bootstrapping计算的，对于较大的数据集，
它可能是时间密集型的。因此，有可能禁用它们
"""
sns.relplot(x="timepoint", y="signal", ci=None, kind="line", data=fmri)


"""
另一个不错的选择，特别是对于较大的数据，
是通过绘制标准差而不是置信区间来表示分布在每个时间点的分布范围:
"""
sns.relplot(x="timepoint", y="signal", kind="line", ci="sd", data=fmri)


"""
要完全关闭聚合，将estimator参数设置为None。
当数据在每个点有多个观察值时，这可能会产生奇怪的效果。
"""
sns.relplot(x="timepoint", y="signal", estimator=None, kind="line", data=fmri)

"""hue
添加一个具有两个级别的hue语义
，将图分割为两条线和错误带，每条线用不同的颜色表示它们对应的数据子集
"""
sns.relplot(x="timepoint", y="signal", hue="event", kind="line", data=fmri)


"""
多种标记和风格区分
"""
sns.relplot(x="timepoint", y="signal", hue="region", style="event",
            dashes=False, markers=True, kind="line", data=fmri)


#绘制日期格式
df = pd.DataFrame(dict(time=pd.date_range("2017-1-1", periods=500),
                       value=np.random.randn(500).cumsum()))
g = sns.relplot(x="time", y="value", kind="line", data=df)
g.fig.autofmt_xdate()

#多子图
sns.relplot(x="timepoint", y="signal", hue="subject",
            col="region", row="event", height=3,
            kind="line", estimator=None, data=fmri)



"""
检查一个变量的多个级别的效果时，在列上对该变量进行切面处理，
然后将切面“包装”到行中是一个好主意
"""
sns.relplot(x="timepoint", y="signal", hue="event", style="event",
            col="subject", col_wrap=5,
            height=3, aspect=.75, linewidth=2.5,
            kind="line", data=fmri.query("region == 'frontal'"))