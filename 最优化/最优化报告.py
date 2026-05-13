import scipy.optimize as opt
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
def fobj(x):
    # 目标函数
    return x[0] + 10 * x[1]
def neq(x):
    #约束
    y = np.zeros([4, ])
    y[0] = x[0] + x[1] - 1
    y[1] = -(x[0] + x[1] - 1)
    y[2] = -x[0]
    y[3] = -x[1]
    return y
def proj_i(x):
    y = x.copy()
    for i in range(len(x)):
        y[i] = max(x[i], 0)
    return y
root = np.array([1.0, 0.0])
np.random.seed(8286) #我的学号
rt = np.random.randn(2)
it = 20
lya = np.ones([it, 1])
def exct_pnlt(x, c):
    # 等价定义二次罚函数
    z = fobj(x)
    v = proj_i(neq(x))
    M = la.norm(v) * c
    z = z + M
    return z
# 循环迭代
for i in range(it):
    c = (i + 1) * 10
    def fmin(x):
        return (exct_pnlt(x, c))
    sol = opt.minimize(fmin, rt, method='bfgs', tol=1e-8)
    rt = sol.x
    lya[i] = la.norm(rt - root) ** 2
print(rt)
#  绘图
plt.figure()
plt.semilogy(lya, '.-')
plt.legend(["prim", "dual", "kkt"])
plt.grid(True)
plt.show()