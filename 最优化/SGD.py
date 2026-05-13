#最小二乘问题
import numpy as np
import matplotlib.pyplot as plt

dim = 3
num = 30
np.random.seed(1)  # 固定随机种子
x = np.random.randn(num, dim)  # 状态数据
y = np.random.randn(num, 1) / 2  # 标签数据
init = np.random.randn(dim, 1)  # 初始点


def gobj(theta, xi):  # 随机梯度函数
    z = x[xi, :]
    out = 2 * (np.dot(z, theta) - y[xi]) * z.T
    return (out)


def sgd(gobj, init, num):  # 随机梯度求解器

    root = gobj(init, 1)  # 迭代点估计
    dim = len(root)
    it = 100000
    i = 0
    path = np.zeros([it, dim])  # 记录每一步的迭代点
    while i < it - 1:
        i = i + 1
        a = 1 / (i + 3) ** (8 / 9)
        xi = np.random.randint(0, num)  # 生成随机数
        root = root - a * gobj(root, xi)  # 随机梯度步骤
        for j in range(dim):
            path[i, j] = root[j]

    return (root, path)


[v, path] = sgd(gobj, init, num)

sol = np.dot(np.linalg.inv(np.dot(x.T, x)), np.dot(x.T, y))  # 计算精确解

d=np.zeros([100000,1])
for i in range(100000):
    d[i]=np.linalg.norm(sol.T-path[i,:],2)

plt.loglog(d,'r.-')
plt.grid(True)
plt.show()

#逻辑回归问题
import numpy as np
import matplotlib.pyplot as plt

dim = 2
num = 30
np.random.seed(1)  # 固定随机种子
x = np.random.randn(num, dim)  # 状态数据
sol = np.arange(dim + 1)

y = np.zeros([num, 1])
for i in range(num):
    if np.dot(x[i, :], sol[0:dim]) + sol[dim] < 0:
        y[i] = 0
    else:
        y[i] = 1

init = np.random.randn(dim + 1)  # 初始点


def gobj(theta, xi):  # 随机梯度函数
    z = x[xi, :]
    dim = len(theta) - 1
    out = theta.copy()
    et = np.exp(np.dot(theta[00:dim], z) + theta[dim])
    out[0:dim] = y[xi] * z - et / (1 + et) * z
    out[dim] = y[xi] - et / (1 + et)
    return (-out)


def sgd(gobj, init, num):  # 随机梯度求解器
    dim = len(init) - 1
    root = init.copy()  # 迭代点估计

    it = 100000
    i = 0
    path = np.zeros([it, dim + 1])  # 记录每一步的迭代点
    while i < it - 1:
        i = i + 1
        # a=1/(i+3)**(8/9)
        a = 1 / num
        xi = np.random.randint(0, num)  # 生成随机数
        root = root - a * gobj(root, xi)  # 随机梯度步骤
        for j in range(0, dim + 1):
            path[i, j] = root[j]

    return (root, path)


[v, path] = sgd(gobj, init, num)
/ tmp / ipykernel_3575 / 3764578963.
py: 24: DeprecationWarning: Conversion
of
an
array
with ndim > 0 to a scalar is deprecated, and will error in future.Ensure you extract a single element from your array before performing this operation.(Deprecated NumPy 1.25.)out[dim] = y[xi] - et / (1 + et)

d = np.zeros([100000, 1])
y_test = np.zeros([num, 1])
for i in range(num):
    if np.dot(x[i, :], v[0:dim]) + v[dim] < 0:
        y_test[i] = 0
    else:
        y_test[i] = 1

sum(np.abs(y_test - y)) / num  # 错误率
array([0.])