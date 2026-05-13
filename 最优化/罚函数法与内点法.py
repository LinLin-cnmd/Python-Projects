#报告：同一个函数，进行精确和非精确罚函数方法

#非精确(二次)罚方法
import scipy.optimize as opt
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
def fobj(x):
    # 定义目标函数
    return(x[0]**2+x[1]**2-x[2])
def neq(x):
    # 定义不等式约束
    y=np.zeros([3,])
    y[0]=x[2]-x[0]+1
    y[1]=x[2]+x[0]+1
    y[2]=x[2]-x[1]+1
    return(y)
def proj_i(x):
    # 定义正卦限锥的投影
    lth=x.shape
    y=x
    for i in range(lth[0]):
        y[i]=np.max([x[i],0])
    return(y)
def int_i(x):
    # 定义正卦限锥的内点
    lth=x.shape
    y=x
    for i in range(lth[0]):
        y[i]=-np.log(x[i])
    return(y)
# 测试
root=np.array([0,0,-1])
print(fobj(root))
print(neq(root))
print(np.exp(-3.8))
print(proj_i(np.array([-1,2,0])))
print(int_i(np.array([3,2,1])))
rt = np.ones([3]) * 10
it = 20
lya = np.ones([it, 1])
def quad_pnlt(x, c):
    # 等价定义二次罚函数
    z = fobj(x)
    v = proj_i(neq(x))
    M = np.power(la.norm(v), 2) * c
    z = z + M
    return (z)
# 循环迭代
for i in range(it):
    c = (i + 3) ** 4
    def fmin(x):
        return (quad_pnlt(x, c))
    sol = opt.minimize(fmin, rt, method='bfgs')
    rt = sol.x
    lya[i] = la.norm(rt - root) ** 2
print(rt)
#  绘图
plt.semilogy(lya, '.-')
plt.legend(["prim", "dual", "kkt"])
plt.grid(open)

#精确罚函数法
rt = np.ones([3]) * 10
it = 20
lya = np.ones([it, 1])
def exct_pnlt(x, c):
    # 等价定义二次罚函数
    z = fobj(x)
    v = proj_i(neq(x))
    M = la.norm(v) * c
    z = z + M
    return (z)
# 循环迭代
for i in range(it):
    c = (i + 2) / 3
    def fmin(x):
        return (exct_pnlt(x, c))
    sol = opt.minimize(fmin, rt, method='bfgs')
    rt = sol.x
    lya[i] = la.norm(rt - root) ** 2
print(rt)
#  绘图
plt.semilogy(lya, '.-')
plt.legend(["prim", "dual", "kkt"])
plt.grid(open)

#内点法
rt = np.ones([3]) * 10
it = 20
lya = np.ones([it, 1])
def br(x, c):
    # 等价定义二次罚函数
    z = fobj(x)
    v = proj_i(neq(x))
    M = sum(v) / c
    z = z + M
    return (z)
# 循环迭代
for i in range(it):
    c = 10 / (i + 2) ** 2
    def fmin(x):
        return (br(x, c))
    sol = opt.minimize(fmin, rt, method='bfgs')
    rt = sol.x
    lya[i] = la.norm(rt - root) ** 2
print(rt)
#  绘图
plt.semilogy(lya, '.-')
plt.legend(["prim", "dual", "kkt"])
plt.grid(open)
