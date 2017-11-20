# coding: utf-8
# 赶只鸡 算法
from sklearn import datasets
# import matplotlib.pyplot as plt

# 构造用于回归的数据make_regression
# 参数的意思：100个例子，1种特征，1种输出，噪声的大小为2
X, y = datasets.make_multilabel_classification()
print(X, y)

# plt.plot(X, y, 'o')
# plt.show()
