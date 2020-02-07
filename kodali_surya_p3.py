'''
    ModSim 5790 P3: Pendulum
    Created by: Surya Kodali
'''

import numpy as np 
import scipy.integrate as integrate
import matplotlib.pyplot as plt 


def choirBoy(t, y):
    return

def hooligan(t, y, mu, g, L):
    theta, w = y[0], y[1]
    # print(mu, g, L)
    dy = np.array(w, -mu * w - g * np.sin(theta) / L)
    return (dy)
    
def pendulum(thetaZero=30.0, damp=0.0, timeSpan=20.0, length=0.45, gravity=9.80, wZero=0.0):
    ''' ___________________________________________________________________________________
        All input parameters are of type float.
        thetaZero: initial displacement angle (degrees)
        damp: damping coefficient
        timeSpan: time length for simulation
        length: length of pendulum
        gravity: acceleration due to gravity
        wZero: initial angular velocity (degrees/s) (positive is cw)
        ___________________________________________________________________________________
        This function displays an animation comparing the pendulum motion 
        as described by two different versions of the second-order
        nonlinear ordinary differential equation:
        
        1. d^2(theta)/dt^2 + mu * d(theta)/dt + g * sin(theta)/L = 0
        
        Assuming neglibigle mass, small theta, and no damping the above 
        equation is simplified and can be analytically solved to get:
        
        2. theta = theta0 * cos(sqrt[g/L * t])
        
        Transforming eq1, we will numerically solve this system:
        
        3. d(theta)/dt = w                          theta(0) = theta0
           dw/dt = -mu * w - g * sin(theta)/L       w(0) = w0
           
           let y be the a 3x1 matrix of the original dependent variables
           theta and w. dy/dt is 3x1 matrix of the system of ODEs.
           y(0) = [thetaZero, wZero]
        ___________________________________________________________________________________
    '''
    # converts to radians
    thetaRad = np.radians(thetaZero)
    wRad = np.radians(wZero)
    # creates time range with increments
    time = np.linspace(0,timeSpan, 100)
    # assigns damp, gravity, and length to be used outside of scope
    mu_global, g_global, L_global = damp, gravity, length
    # gets solution for initial value problem for our system, args* was not working
    res = integrate.solve_ivp(fun=lambda t, y: hooligan(t, y, damp, gravity, length), t_span=(0, timeSpan), y0=(thetaRad,wRad), t_eval=time)
    displayMotion(res)

def displayMotion(res):
    plt.plot(res.t, np.degrees(res.y[0]))
    plt.plot(res.t, np.degrees(res.y[1]))
    plt.xlabel('time')
    plt.ylabel('angle or angluar velocity')
    plt.show()

if __name__ == '__main__':
    pendulum(damp = 0.2, wZero = 50, timeSpan=100)
    pass