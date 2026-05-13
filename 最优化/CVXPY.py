import numpy as np
import cvxpy as cp
cp.installed_solvers()
'''无约束优化'''
'''最小二乘法'''
# Import packages.
import cvxpy as cp
import numpy as np
# Generate data.
m = 9
n = 3
np.random.seed(1)
A = np.random.randn(m, n)
b = np.random.randn(m)
# Define and solve the CVXPY problem.
x = cp.Variable(n)
cost = cp.sum_squares(A @ x - b)
prob = cp.Problem(cp.Minimize(cost))
prob.solve()
# Print result.
print("\nThe optimal value is", prob.value)
print("The optimal x is")
print(x.value)
print("The norm of the residual is ", cp.norm(A @ x - b, p=2).value)

# Import packages.
import cvxpy as cp
import numpy as np
# Generate data.
m = 2
n = 3
np.random.seed(1)
A = np.random.randn(m, n)
b = np.random.randn(m)
# Define and solve the CVXPY problem.
x = cp.Variable(n)
cost = cp.sum_squares(A @ x - b)
prob = cp.Problem(cp.Minimize(cost))
prob.solve()
# Print result.
print("\nThe optimal value is", prob.value)
print("The optimal x is")
print(x.value)
print("The norm of the residual is ", cp.norm(A @ x - b, p=2).value)

'''指数分布的极大似然估计'''
# Import packages.
import cvxpy as cp
import numpy as np
# Generate data.
n=1000
lmbd_star=3
data = np.random.exponential(lmbd_star,n)
lmbd=cp.Variable(1, pos=True)
# Define and solve the CVXPY problem.
cost = cp.sum(-data*lmbd + cp.log(lmbd))
prob = cp.Problem(cp.Maximize(cost))  # Maximum Likelihood Estimation
prob.solve()
# Print result.
print("\n The optimal value is", prob.value)
print("The optimal lambda is")
print(1/lmbd.value)
print(sum(data)/n)

'''线性锥约束优化问题'''
'''线性规划'''
# Import packages.
import cvxpy as cp
import numpy as np
# Generate a random non-trivial linear program.
m = 4
n = 3
np.random.seed(1)
s0 = np.random.randn(m)
lamb0 = np.maximum(-s0, 0)
s0 = np.maximum(s0, 0)
x0 = np.random.randn(n)
A = np.random.randn(m, n)
b = A @ x0 + s0
c = -A.T @ lamb0
# Define and solve the CVXPY problem.
x = cp.Variable(n)
prob = cp.Problem(cp.Minimize(c.T@x),[A @ x <= b])
prob.solve()
# Print result.
sol=prob.solution
print("原始变量",sol.primal_vars)
print("对偶变量",sol.dual_vars)
print("最优值",sol.opt_val)
print("求解状况:",sol.status)

# Import packages.
import cvxpy as cp
import numpy as np
# Generate a random non-trivial linear program.
m = 4
n = 3
np.random.seed(1)
s0 = np.random.randn(m)
lamb0 = np.maximum(-s0, 0)
s0 = np.maximum(s0, 0)
x0 = np.random.randn(n)
A = np.random.randn(m, n)
b = A @ x0 + s0
c = -A.T @ lamb0
# Define and solve the CVXPY problem.
x = cp.Variable(n)
prob = cp.Problem(cp.Minimize(c.T@x),[cp.NonPos(A @ x - b)])
prob.solve()
# Print result.
sol=prob.solution
print("原始变量",sol.primal_vars)
print("对偶变量",sol.dual_vars)
print("最优值",sol.opt_val)
print("求解状况:",sol.status)

'''线性二阶椎规划'''
# Import packages.
import cvxpy as cp
import numpy as np
# Generate a random non-trivial linear program.
A =np.array([[1,1,0],[1,-1,0]])
b =np.array([1,0])
c = np.array([[0,0,1]])
p=c.copy()
q=0
# Define and solve the CVXPY problem.
x = cp.Variable(3)
prob = cp.Problem(cp.Minimize(c@x),[ cp.SOC(p@x-q, A@x-b)])
prob.solve()
# Print result.
sol=prob.solution
print("原始变量",sol.primal_vars)
print("对偶变量",sol.dual_vars)
print("最优值",sol.opt_val)
print("求解状况:",sol.status)  # 可以取得最优解

#小例子
# Import packages.
import cvxpy as cp
import numpy as np
# Generate a random non-trivial linear program.
A =np.array([[1,1,0]])
b =np.array([[1]])
c = np.array([[0,0,1]])
p=c.copy()*0
q=10
# Define and solve the CVXPY problem.
x = cp.Variable(3)
prob = cp.Problem(cp.Minimize(c@x),[ cp.SOC(p@x-q, A@x-b ) ])
prob.solve()
# Print result.
sol=prob.solution
print("原始变量",sol.primal_vars)
print("对偶变量",sol.dual_vars)
print("最优值",sol.opt_val)
print("求解状况:",sol.status) # 约束集合不可行

''''''