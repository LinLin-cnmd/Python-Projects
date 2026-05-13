import numpy as np
np.random.seed(0)
arr1 = np.random.randn(3,3)
arr2 = np.random.randint(0,100,(3,3))
for num in arr2:
    print(*num)