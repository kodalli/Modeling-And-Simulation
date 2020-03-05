import numpy as np 

# with a loop
# nsum = 0
# for i in range(10000):
#     total = 0
#     count = 0
#     while(total <= 1):
#         total += np.random.uniform()
#         count+=1
#     nsum += count
#     print(nsum/(i+1))
    

rnums = np.random.rand(100)
#print(rnums)
cnums = np.cumsum(rnums)
#print(cnums)
print(np.where(cnums >= 1, cnums))