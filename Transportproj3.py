import numpy as np
import matplotlib.pyplot as plt
import time as time
import concurrent.futures
import multiprocessing

# R = 1e-4  # cm
# a = 40e-4  # cm
# b = 50e-4  # cm
# # k = (0.0921e-3)/3600  # s^-1
c0 = 2.83993085e-1  # umol/cm^3
# c1 = 2.53565254e-3  # umol/cm^3


D = 0.9e-12  # cm^2/s
maxiter = 10000
b = 50e-4
maxt = 1000


def fun(t):
    a = 0
    total = 0
    for n in range(1, maxiter):
        total += ((b*np.cos(n*np.pi) - a)/n)**2 * \
            np.exp(-D * n**2 * t/(b-a)**2)
    return float(1 - 6/(np.pi**2 * (a**2 + a*b + b**2)) * total)


def fun1(t):
    a = 10e-4
    total = 0
    for n in range(1, maxiter):
        total += ((b*np.cos(n*np.pi) - a)/n)**2 * \
            np.exp(-D * n**2 * t/(b-a)**2)
    return float(1 - 6/(np.pi**2 * (a**2 + a*b + b**2)) * total)


def fun2(t):
    a = 25e-4
    total = 0
    for n in range(1, maxiter):
        total += ((b*np.cos(n*np.pi) - a)/n)**2 * \
            np.exp(-D * n**2 * t/(b-a)**2)
    return float(1 - 6/(np.pi**2 * (a**2 + a*b + b**2)) * total)


def fun3(t):
    a = 45e-4
    total = 0
    for n in range(1, maxiter):
        total += ((b*np.cos(n*np.pi) - a)/n)**2 * \
            np.exp(-D * n**2 * t/(b-a)**2)
    return float(1 - 6/(np.pi**2 * (a**2 + a*b + b**2)) * total)


def fun4(t):
    a = 35e-4
    total = 0
    for n in range(1, maxiter):
        total += ((b*np.cos(n*np.pi) - a)/n)**2 * \
            np.exp(-D * n**2 * t/(b-a)**2)
    return float(1 - 6/(np.pi**2 * (a**2 + a*b + b**2)) * total)


def fun5(t):
    a = 40e-4
    total = 0
    for n in range(1, maxiter):
        total += ((b*np.cos(n*np.pi) - a)/n)**2 * \
            np.exp(-D * n**2 * t/(b-a)**2)
    return float(1 - 6/(np.pi**2 * (a**2 + a*b + b**2)) * total)


def fun6(t):
    a = 40e-4
    radius = np.linspace(0.1e-4, 50-4, 10)
    total = 0
    output = np.zeros((len(radius)))
    for i, r in enumerate(radius):
        for n in range(1, maxiter):
            total += ((b*np.cos(n*np.pi) - a)/n) * \
                np.exp(-D * n**2 * t/(b-a)**2) * np.sin(n*np.pi*(r-a))
        output[i] = -c0*(1 + 2*np.pi/r * total) + c0
    return output


def main():
    """
    # pool = multiprocessing.Pool()
    # result = pool.map(fun, tspace)

    # pool1 = multiprocessing.Pool()
    # res1 = pool1.map(fun1, tspace)

    # pool2 = multiprocessing.Pool()
    # res2 = pool2.map(fun2, tspace)

    # pool3 = multiprocessing.Pool()
    # res3 = pool3.map(fun3, tspace)

    # pool4 = multiprocessing.Pool()
    # res4 = pool4.map(fun4, tspace)

    # pool5 = multiprocessing.Pool()
    # res5 = pool5.map(fun5, tspace)
    # # with concurrent.futures.ProcessPoolExecutor() as executor:
    # #     res = executor.map(fun, tspace)
    # # print(list(res))
    # somelist = list(result)
    # somelist1 = list(res1)
    # somelist2 = list(res2)
    # somelist3 = list(res3)
    # somelist4 = list(res4)
    # somelist5 = list(res5)
    # plt.plot(tspace/3600, somelist, tspace/3600, somelist1, tspace/3600,
    #          somelist2, tspace/3600, somelist4, tspace/3600, somelist5, tspace/3600, somelist3)
    # plt.title(
    #     f'Fractional mass transfer vs. time for particle of radius {b*10**4} µm')
    # plt.xlabel('time(hr)')
    # plt.ylabel('M(t)/M0')
    # plt.legend(['a=0µm ', 'a=10µm', 'a=25µm', 'a=35µm', 'a=40µm', 'a=45µm'])
    # plt.show()
    """
    tspace = np.linspace(0, 3600*24*3, maxt)
    pool = multiprocessing.Pool()
    
    result = pool.map(fun6, tspace)
    somelist = list(result)
    radius = np.linspace(0, 50e-4, 10)
    plt.plot(radius, somelist[-1])
    plt.title(
        f'Concentration vs. position for particle of radius {b*10**4} µm')
    plt.xlabel('position (cm)')
    plt.ylabel('µmol/cm^3')
    plt.legend(['a=40µm'])
    plt.show()


if __name__ == '__main__':
    main()
