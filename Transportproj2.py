from scipy.optimize import fmin 
import numpy as np  

V = 5*3785.41 # volume ml
A = 2500 # area cm^2
l = 2 # length cm
time = np.arange(25,225,25) # hr
cl1 = [2.7682E-07, 2.7684E-07, 2.7687E-07, 2.7688E-07, 2.7690E-07, 2.7694E-07, 2.7695E-07, 2.7697E-07] # mol/cm^3
cl2exp = [5.1993E-08, 9.4227E-08, 1.2854E-07, 1.5640E-07, 1.7905E-07, 1.9745E-07, 2.1239E-07, 2.2453E-07];

cl2pred = np.zeros(len(cl1));

def f(Deff):
    diffsum = 0
    for i in range(len(time)):
        cl2pred[i] =  cl1[i]*(1-np.exp(-Deff*A/(V*l)*time[i]));
        diffsum += (10E9 * (cl2exp[i] - cl2pred[i]))**2;
    return diffsum

Deff = fmin(f, 0.5)

print(Deff)