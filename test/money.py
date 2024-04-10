
# 导入必要的库
import pandas as pd
from statsmodels.formula.api import glm
from statsmodels.genmod.families import Binomial, Gaussian

# 加载Excel文件
df = pd.read_excel(r'C:\Users\Administrator\Documents\GitHub\TranquilEcho\test\TRYxmxhy.xlsx')

# 数据预处理
# 添加一个新列来表示小黄鱼的出现与否（1表示出现，0表示未出现）
df['Presence'] = df['SR'].apply(lambda x: 1 if x > 0 else 0)

# 环境因子选择
# 假设所有列除了'Month'和'SR'都是环境因子
environmental_factors = df.columns.drop(['Month', 'Site', 'SR'])

# 构建两阶GAM模型
# 第一阶段：模拟鱼的出现概率
formula_presence = 'Presence ~ ' + ' + '.join(environmental_factors)
gam1 = glm(formula_presence, data=df, family=Binomial()).fit()

# 第二阶段：模拟鱼的丰度
# 只考虑鱼出现的情况
df_present = df[df['SR'] > 0]
formula_abundance = 'SR ~ ' + ' + '.join(environmental_factors)
gam2 = glm(formula_abundance, data=df_present, family=Gaussian()).fit()

# 输出模型摘要
print('模型1（出现概率）摘要:')
print(gam1.summary())
print('\n模型2（丰度）摘要:')
print(gam2.summary())