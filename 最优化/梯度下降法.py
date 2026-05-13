#常步长方法
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
def fobj(x):  # 目标函数
    return(x[0]**2+4*x[1]**2)
def gobj(x):  # 目标函数的梯度
    return(np.array([2*x[0],8*x[1]]))

def fmin_grad_const(fobj,gobj,init):
    root=init.copy()
    j=0
    while la.norm(gobj(root))>1e-6:
        root=root - gobj(root)/8
        j=j+1
        if  j> 1e4:
            break
    return(root)
x0 = np.array([[8], [2]])
x_min = fmin_grad_const(fobj, gobj, x0)
print("极小值点：", x_min)

#最速下降法 (精确线搜索)
import numpy as np
import numpy.linalg as la
def fobj(x):   # 目标函数
    return(x[0]**2+4*x[1]**2)
def gobj(x):   # 目标函数的梯度
    return(np.array([2*x[0],8*x[1]]))

def hjfg_drct(fobj,intv,point,direct):
    a1=intv[0]
    a2=intv[1]zz
    r=1-(np.sqrt(5)-1)/2
    b=a1+r*(a2-a1)
    c=a2+r*(a1-a2)
    d=abs(a1-a2)
    while d>=1e-6:
        if fobj(point + b*direct)>fobj(point+c*direct):
            a1=b
        else:
            a2=c
        b=a1+r*(a2-a1)
        c=a2+r*(a1-a2)
        d=abs(a1-a2)
    return((b+c)/2)

def fmin_grad_hjfg(fobj,gobj,init,hjfg_drct):
    root=init.copy()
    while la.norm(gobj(root))>1e-6:
        direct=-gobj(root)
        a=hjfg_drct(fobj,[0,1/2],root,direct)
        root=root - gobj(root)*a
    return(root)

init=np.array([[8],[2]])
v=fmin_grad_hjfg(fobj,gobj,init,hjfg_drct)
print(v)

#Armijo 准则线搜索
import numpy as np
import numpy.linalg as la
def fobj(x):   # 目标函数
    return(x[0]**2+4*x[1]**2)
def gobj(x):   # 目标函数的梯度
    return(np.array([2*x[0],8*x[1]]))

def armijo_drct(fobj,gobj,point,direct):
    c=0.1
    m=1
    a=0.75
    while  fobj(point+a**m*direct)> fobj(point)- c*a**m*la.norm(gobj(point))**2:
        m=m+1
    return(a**m)

def fmin_grad_armijo(fobj,gobj,init,armijo_drct):
    root=init.copy()
    while la.norm(gobj(root))>1e-6:
        direct= -gobj(root)
        a=armijo_drct(fobj,gobj,root,direct)
        root=root - gobj(root)*a
    return(root)

init=np.array([[8],[2]])
v=fmin_grad_armijo(fobj,gobj,init,armijo_drct)
print(v)

#应用A: 对数据进行线性最小二乘法估计
import numpy as np
import numpy.linalg as la

num= 1000; dim=10;
A =np.matrix( np.random.randn(num,dim))
x =np.matrix( np.random.randn(dim,1))
b =A*x

def fobj(x):
    return(la.norm(A*x-b)**2)

def gobj(x):
    return(2*A.T*(A*x-b) )

def armijo_drct(fobj,gobj,point,direct):
    c=0.5
    m=0
    a=0.9
    while  fobj(point+a**m*direct) > fobj(point)- c*a**m*la.norm(gobj(point))**2:
        m=m+1
    return(a**m)

def fmin_grad_armijo(fobj,gobj,init,armijo_drct):
    root=init.copy()
    itmax=1e2
    it=0
    while la.norm(gobj(root))>1e-6:
        direct= -gobj(root)
        a=armijo_drct(fobj,gobj,root,direct)
        root=root - gobj(root)*a
        it=it+1
        if it>itmax:
            print("Exceed the maximal iteration")
            break
    return(root)

init= np.ones([dim,1])
v=fmin_grad_armijo(fobj,gobj,init,armijo_drct)
la.norm(gobj(v))