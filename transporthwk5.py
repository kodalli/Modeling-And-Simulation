from scipy import special
from scipy.optimize import fsolve
import numpy as np

# Ti = 45
# Tf = 5
# a = 0.5e-6
# L = 0.1

# def laplace(x, t):
#     sum = 0
#     for j in range(1, 100000):
#         sum += (-1)**j * (special.erfc((2*j+1)*(L-x)/(2*(a*t)**0.5)) + special.erfc((2*j+1)*(L+x)/(2*(a*t)**0.5)))
#     output = (1-sum)*(Ti-Tf) + Tf
#     return output
# # t in seconds, x in meters
# def fourier(x, t):
#     sum = 0
#     for j in range(1, 1000000, 2):
#         sum += 1/j * (np.sin(j*np.pi*x/(2*L))*np.exp(-(j*np.pi/(2*L))**2 * a*t))
#     sum = sum * 4/np.pi
#     sum = sum * (Ti-Tf) + Tf
#     return sum
# #print(laplace(0.1, 2*60*60))
# print(fourier(0.05, 1800))
# print(fourier(0.1, 7200))
# print(fourier(0.1, 1000000)) # Steady state


def f(p):
    t = p
    ho = 0.026/(1+2*t)*0.26*((1+2*t)/(1.8e-5 / 1.16))**0.6 * 0.72**0.37
    return(
        -1/1.18 + 1/22 + 1/0.2 * np.log(1+2*t) + 1/(1+2*t)*1/ho
    )


t = fsolve(f, (0.00001))
print(t)
