import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pygam

# 读取Excel数据
data = pd.read_excel(r'C:\Users\Administrator\Documents\GitHub\TranquilEcho\test\TRYxmxhy.xlsx')

# 确保数据中包含以下连续变量，并移除其他非数值列（如Month和Site）
continuous_vars = ['Deep', 'Temperature', 'Ph', 'DO', 'Conductivity', 'Chlorophyll_a', 'NH3_N', 'TN', 'TP']
data = data[continuous_vars + ['SR']].dropna()  # 假设'SR'为目标变量，移除含有缺失值的行

# 定义一个拟合GAM模型的函数
def fit_and_plot_gam(target_var='SR', predictor_vars=continuous_vars, family=pygam.families.Gaussian()):
    model = pygam.PYGAM([pygam.s(var) for var in predictor_vars], family=family, method='REML')
    model.fit(data[predictor_vars + [target_var]])
    
    # 输出模型摘要信息
    print(pygam.summary(model))

    # 绘制平滑项
    fig, axs = plt.subplots(len(predictor_vars), 1, figsize=(10, len(predictor_vars)*5))
    for i, pred_var in enumerate(predictor_vars):
        ax = axs[i]
        pygam.plots.plot_smooth(model, ax=ax, x=pred_var, y=target_var)
        ax.set_xlabel(pred_var)
        ax.set_ylabel(target_var)
    
    plt.tight_layout()
    plt.savefig('GAM模型.tiff', dpi=300, format='tiff', compress='lzw')

# 调用函数拟合并绘制模型
fit_and_plot_gam(target_var='SR')

# 若需要使用Tweedie分布或Poisson分布，需根据实际分布参数调整family参数
# 例如，若目标变量服从Tweedie分布，可能需要自定义一个分布类或查找是否有现成的库支持