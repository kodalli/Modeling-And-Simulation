
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.optimize import fsolve
from difflib import SequenceMatcher

str1 = 'hello'
str2 = 'adsgasdfaerefheowefhoealeohae'
seq = SequenceMatcher(None, str1, str2)
print(seq.ratio())
# k1 = 10
# k2 = 0.192


# def f(t, y):
#     '''
#         Equations:
#         k1 = 10
#         k2 = 0.192
#         dCa/dt = -k1*Ca
#         dCb/dt = -k2 + k1*Ca

#     '''
#     Ca, Cb = y
#     df = [
#         -k1*Ca,
#         -k2 + k1*Ca
#     ]
#     return df


# time = np.arange(0, 24, 0.001)
# res = integrate.solve_ivp(fun=f, y0=(1, 0), t_span=(
#     np.min(time), np.max(time)), method='RK45', t_eval=time)
# plt.plot(res.t, res.y[1])
# plt.xlabel('time (hrs)')
# plt.ylabel('Cb')
# plt.show()
# print(res.y[1][np.where(res.t == 0.5)])
# print(res.y[0][np.where(res.t == 0.5)])
# limit = 0
# for index, item in enumerate(res.y[1]):
#     if(np.abs(item - limit) < 0.001):
#         print(res.t[index])

# def f(Cc, t):
#     Co = 0.5/1000
#     return - 0.9*12/np.pi * np.cos(np.pi*t/12) - 0.5*np.log(Co + 2*Cc) + 0.5*np.log(3*Co)


# t = np.arange(0, 48, 0.01)
# Cc = [fsolve(f, 0.01, i) for i in t]
# plt.plot(t, Cc)
# plt.show()
# T0 = 300


# def f(X, y):
#     T = T0 + 500*X
#     v0 = 20
#     k = 0.133*np.exp(31400/8.314*(1/T0 - 1/T))
#     return(
#         v0 * (1+X)*T/k/(1-X)/T0
#     )


# X = np.arange(0, 0.8, 0.01)
# res = integrate.solve_ivp(fun=f, y0=(0, 0), t_span=(
#     X[0], X[-1]), method='RK45', t_eval=X)

# plt.plot(res.y[0], res.t*500+T0)
# plt.show()
