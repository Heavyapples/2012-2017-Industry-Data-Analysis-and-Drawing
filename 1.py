# -*- coding: utf-8 -*-
import pandas as pd  # 导入 pandas 库，用于数据处理
import numpy as np  # 导入 numpy 库，用于数组操作
import matplotlib.pyplot as plt  # 导入 matplotlib 的 pyplot 模块，用于绘图
import matplotlib  # 导入 matplotlib 库，用于设置字体等属性

font = {'family': 'SimHei'}  # 设置字体为 SimHei，以便图表中显示中文
matplotlib.rc('font', **font)  # 应用字体设置

# 从 excel 文件中读取数据
data = pd.read_excel('公司净利润数据表.xlsx')
td = pd.read_excel('申万行业分类表.xlsx')

name = td['行业名称'].value_counts()  # 统计各行业的出现次数
name = list(name.index)  # 提取行业名称作为列表

D = np.zeros((len(name), 7))  # 初始化一个零矩阵，存储各行业在 2011-2017 年的净利润
D1 = np.zeros((len(name), 6))  # 初始化一个零矩阵，存储各行业在 2011-2016 年的净利润增长率

# 计算各行业在 2011-2017 年的净利润
for i in range(len(name)):
    s = td.loc[td['行业名称'].values == name[i], '股票代码'].values  # 获取当前行业的所有股票代码
    for y in range(2011, 2018):
        date = str(y) + '-12-31'  # 设置日期格式
        stk = data.loc[data['Accper'].values == date, 'Stkcd'].values  # 获取对应日期的股票代码
        lr = data.loc[data['Accper'].values == date, 'B002000101'].values  # 获取对应日期的净利润
        S = pd.Series(lr, index=stk)  # 创建一个以股票代码为索引、净利润为值的 pandas Series
        valid_s = [stock_code for stock_code in s if stock_code in S.index]  # 仅保留存在于 S 索引中的股票代码
        D[i, y - 2011] = S[valid_s].sum()  # 计算当前行业在当前年份的净利润总和

# 计算各行业在 2011-2016 年的净利润增长率
for k in range(len(name)):
    D1[k, :] = (D[k, 1:] - D[k, :-1]) / D[k, :-1]  # 计算净利润增长率
D1 = pd.DataFrame(D1, index=name) # 将净利润增长率数据转换为 DataFrame，行业名称作为索引

'''
for i in range(6):
    plt.figure(i)
    q=D1[i].sort_values()[-8:]
    plt.bar([1,2,3,4,5,6,7,8],q.values)
    plt.xticks([1,2,3,4,5,6,7,8],q.index,rotation=40)
'''

# 绘制各行业在 2012-2017 年的净利润增长率排名前 8 的柱状图
plt.figure(1)
plt.figure(figsize=(10, 8))

# 用一个 for 循环创建 6 个子图，分别对应 2012-2017 年的净利润增长率排名前 8 的行业
for i in range(6):
    plt.subplot(3, 2, i + 1)  # 创建一个 3x2 的子图布局，并设置当前子图的位置
    plt.title(str(2012 + i) + '年净利润增长率前8的行业')  # 设置子图标题
    plt.tight_layout()  # 调整子图之间的间距
    q = D1[i].sort_values()[-8:]  # 对净利润增长率进行排序，提取排名前 8 的行业
    plt.bar([1, 2, 3, 4, 5, 6, 7, 8], q.values)  # 创建柱状图，显示前 8 个行业的净利润增长率
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8], q.index, rotation=45)  # 设置 x 轴刻度标签和对应的行业名称，标签旋转 45 度
plt.savefig('1')   # 保存图形为名为 '1' 的文件
