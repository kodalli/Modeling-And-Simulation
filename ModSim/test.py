import numpy as np
H, W = 10, 10
density = 0.6
z = np.random.binomial(1, density, (W, H))
for i in range(int(W/2-2.5), int(W/2+2.5)):
    for j in range(int(H/2-2.5), int(H/2+2.5)):
        if(z[i, j]):
            z[i, j] = 2

# k = z[int(W/2-2.5):int(W/2+2.5), int(H/2-2.5):int(H/2+2.5)] == 1
# print(k)
# z[k] = 2
print(z)
