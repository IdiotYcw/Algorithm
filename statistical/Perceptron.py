# coding: utf-8
# 赶只鸡 算法
import os
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt

# 构造数据
# 参数的意思：100个例子，2种特征，1种输出，噪声的大小为2
# n_s, n_f, n_c, noise = 100, 5, 2, 2
# X, y = datasets.make_sparse_uncorrelated(
#     n_samples=n_s, n_features=n_f)

X = [[1, 2], [2, .5], [1.5, .8], [1, .2], [2, -0.4], [1.5, 0]]
y = [1, 1, 1, -1, -1, -1]
# print(X, y)
X_matrix = np.matrix(X)  # 将list转成numpy array
y_matrix = np.matrix(y)
print(X_matrix.shape, y_matrix.shape)

W = np.zeros((2, 1))
b = 0  # np.zeros((6, 1))
LAP = 1  # 拉普拉斯平滑

# percetron model
percetron = lambda x: 1 if x >= 0 else -1


def update(x, l):
    global W, b
    W = W + (LAP*l*x).T
    b = b + LAP*l
    print('update to: --\n', W, '\n-- and ', b)


def check():
    flag = False
    for d, c in zip(X, y):
        d = np.matrix(d)
        r = np.matmul(d, W)
        if c * percetron(r.prod()+b) < 0:
            flag = True
            update(d, c)
    if not flag:
        print('weight and bias: ', W, b)
        os._exit(0)

if __name__ == '__main__':
    for i in range(1000):
        print('Now is the %s step' % i)
        check()

    plt.plot(X, 'o')
    plt.show()
