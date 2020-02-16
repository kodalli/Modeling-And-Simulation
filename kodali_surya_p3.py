''' ___________________________________________________________________________________
    ModSim 5790 P3: Pendulum
    Created by: Surya Kodali
    Additional help: scipy, matplotlib, numpy documentation, and stackoverflow
    Description: This program takes in user parameters and displays the 
    motion of both a simple harmonic oscillator and an actual pendulum 
    using the anlytical solution and numerical integration.
    ___________________________________________________________________________________
'''

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import math


def pendulum(thetaZero=30.0, damp=0.0, timeSpan=20.0, length=0.45, gravity=9.8, wZero=0.0):
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

           let y be a 1x2 matrix of the dependent variables
           theta and w. dy/dt is 1x2 matrix of the system of ODEs,
           with initial conditions y(0) = [thetaZero, wZero]
        ___________________________________________________________________________________
    '''
    # analytical solution for the motion of a pendulum with assumptions
    def choirBoy(theta0, t):
        return [theta0 * math.cos(math.sqrt(gravity * item / length)) for item in t]

    # jacobian 2x2 matrix for numerical solution
    def jacob(t, y):
        return [[0, 1], [-gravity * math.cos(y[0]) / length, -damp]]

    # system of ordinary differential equations for the motion of a pendulum
    def hooligan(t, y):
        return [y[1], -damp * y[1] - gravity * math.sin(y[0]) / length]

    # check if parameters are negative
    if(damp < 0 or timeSpan < 0 or length < 0 or gravity < 0):
        raise Exception(
            'Cannot enter a negative value for damp, timeSpan, length, or gravity!')

    # converts to radians
    thetaRad, wRad = np.radians(thetaZero), np.radians(wZero)

    # creates time range with increments
    t = np.arange(0, timeSpan, 1/60)

    # solves system of odes with Radau method and jacobian passed through
    res1 = integrate.solve_ivp(fun=hooligan, t_span=[np.min(t), np.max(t)], y0=[thetaRad, wRad],
                               t_eval=t, method='Radau', jac=jacob)

    # res2 is analytical solution
    res2 = choirBoy(thetaRad, res1.t)
    displayMotion(res1, res2, timeSpan, length)


def displayMotion(res1, res2, timeSpan, length):
    '''
        displayMotion takes the results of the two methods of 
        solving for the pendulum motion and animates them.
    '''
    # convert values from polar to cartesian coordinates
    x, y = length*np.sin(res1.y[0]), -length*np.cos(res1.y[0])  # real pendulum
    x2, y2 = length*np.sin(res2), -length*np.cos(res2)  # simple pendulum

    fig, _ = plt.subplots()
    line, = plt.plot([0, x[0]], [0, y[0]], label='real')
    point, = plt.plot([], [], 'ro')
    line2, = plt.plot([0, x2[0]], [0, y2[0]], '--', label='simple')
    point2, = plt.plot([], [], 'bo')
    plt.xlim(-length*1.25, length*1.25)
    plt.ylim(-length*1.25, length*1.25)
    plt.legend()
    plt.xlabel('horizontal position (m)')
    plt.ylabel('vertical position (m)')
    plt.title('Compare motion of simple harmonic oscillator and an actual pendulum')

    # returns each frame of animation
    def animate(frames):
        line.set_data([0, x[frames]], [0, y[frames]])
        point.set_data(x[frames], y[frames])
        line2.set_data([0, x2[frames]], [0, y2[frames]])
        point2.set_data(x2[frames], y2[frames])
        return line, point, line2, point2,

    # gets animation and seperates frames by interval in milliseconds,
    # blit keeps background constant to save resources, 0.8 is a correction factor.
    myAnimation = animation.FuncAnimation(fig, animate, frames=np.arange(0, len(y)-1),
                                          interval=timeSpan/len(y)*1000*0.8, blit=True, repeat=False)

    # show animation and calculate run time, must close window exactly when done to get accurate time
    begin = time.time()
    plt.show()  # plt.show has some blocking mechanism so can't close it within function, plt.ion didn't work
    print('time to exit:', time.time()-begin)


if __name__ == '__main__':
    # pendulum(damp=-0.2, wZero=0, thetaZero=50, length=0.1, timeSpan=20)
    # pendulum(timeSpan=120)
    # pendulum(thetaZero=179.99, damp=0.2, timeSpan=20, wZero=0)
    # pendulum(timeSpan=10, thetaZero=1, length=10)
    # pendulum(thetaZero=180)
    # pendulum(thetaZero=179.99)
    # pendulum(wZero=-517)
    pendulum()
    pass
