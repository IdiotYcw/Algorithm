# coding: utf-8
# 赶只鸡 算法
from sklearn import datasets
import numpy
# import matplotlib.pyplot as plt

# 构造数据
# 参数的意思：100个例子，2种特征，1种输出，噪声的大小为2
n_s, n_f, n_c = 100, 2, 1
X, y = datasets.make_multilabel_classification(
    n_samples=n_s, n_features=n_f, n_classes=n_c)
# print(X, y)
X_matrix = numpy.asarray(X)  # 将list转成numpy array
y_matrix = numpy.asarray(y)
print(X_matrix.shape, y_matrix.shape)

W = numpy.zeros((n_c, n_f))
b = numpy.zeros((n_s, 1))
LAP = 1  # 拉普拉斯平滑

# percetron model
percetron = lambda x: 1 if x >= 0 else 0


# plt.plot(X, y, 'o')
# plt.show()
