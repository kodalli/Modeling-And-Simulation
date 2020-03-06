
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.optimize import fsolve

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

def f(Cc, t):
    Co = 0.5/1000
    return - 0.9*12/np.pi * np.cos(np.pi*t/12) - 0.5*np.log(Co + 2*Cc) + 0.5*np.log(3*Co)


t = np.arange(0, 48, 0.01)
Cc = [fsolve(f, 0.01, i) for i in t]
plt.plot(t, Cc)
plt.show()
