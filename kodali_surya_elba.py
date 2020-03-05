# Surya Kodali
# CBE 5790 Modeling and Simulation
# 2/25/2020
# Midterm Project Elba Epidemic
# Resources: Stackoverflow, Numpy documentation,
# Matplotlib documentation, and Scipy documentation

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

TOTAL_POPULATION = 32000


def ode_model(n, k, tSpan, nMax):
    '''
        n = [HY, HE, HYF, HEF, SY, SE, D, V, I]
        k = [k0, k1, k2, k3, k4, k5]
    '''
    def sick_ode(t, n):
        HY, HYF, HE, HEF, SY, SE, D, V, I = n
        dndt = [
            #HY = -sick -vaccine
            -k[0]*HY*(SY+SE) - k[5]*HY*V,
            #HYF = -sick
            -k[0]*HYF*(SY+SE),
            #HE = -sick -vaccine
            -k[1]*HE*(SY+SE) - k[5]*HE*V,
            #HEF = -sick
            -k[1]*HEF*(SY+SE),
            #SY = +sick - dead - immune
            k[0]*HY*(SY+SE) + k[0]*HYF*(SY+SE) - k[2]*SY - k[4]*SY,
            #SE = +sick - dead - immune
            k[1]*HE*(SY+SE) + k[1]*HEF*(SY+SE) - k[3]*SE - k[4]*SE,
            #D = +dead
            k[2]*SY + k[3]*SE,
            #V = -vaccine
            -k[5]*V*(HY+HE),
            #I = +immune + vaccine
            k[4]*(SY+SE) + k[5]*V*(HY+HE)
        ]
        return dndt

    def jacob(t, n):
        HY, HYF, HE, HEF, SY, SE, D, V, I = n
        dfdy = [
            #HY = -sick -vaccine -k[0]*HY*(SY+SE) -k[5]*HY*V
            [-k[0]*SY - k[0]*SE - k[5]*V, 0, 0, 0, - \
                k[0]*HY, -k[0]*HY, 0, -k[5]*HY, 0],
            #HYF = -sick -k[0]*HYF*(SY+SE)
            [0, -k[0]*SY - k[0]*SE, 0, 0, -k[0]*HYF, -k[0]*HYF, 0, 0, 0],
            #HE = -sick -vaccine -k[1]*HE*(SY+SE) -k[5]*HE*V
            [0, 0, -k[1]*SY - k[1]*SE - k[5]*V, 0, - \
                k[1]*HE, -k[1]*HE, 0, -k[5]*HE, 0],
            #HEF = -sick -k[1]*HEF*(SY+SE)
            [0, 0, 0, -k[1]*SY - k[1]*SE, -k[1]*HEF, -k[1]*HEF, 0, 0, 0],
            # SY = +sick - dead k[0]*HY*(SY+SE) + k[0]*HYF*(SY+SE) -k[2]*SY -k[4]*SY
            [k[0]*SY + k[0]*SE, k[0]*SY + k[0]*SE, 0, 0, k[0]*HY + \
                k[0]*HYF - k[2] - k[4], k[0]*HY + k[0]*HYF, 0, 0, 0],
            # SE = +sick - dead k[1]*HE*(SY+SE) + k[1]*HEF*(SY+SE) -k[3]*SE -k[4]*SE
            [0, 0, k[1]*SY + k[1]*SE, k[1]*SY + k[1]*SE, k[1]*HE + \
                k[1]*HEF, k[1]*HE + k[1]*HEF - k[3] - k[4], 0, 0, 0],
            # D = +dead k[2]*SY + k[3]*SE
            [0, 0, 0, 0, k[2], k[3], 0, 0, 0],
            #V = -vaccine -k[5]*V*(HY+HE)
            [-k[5]*V, 0, -k[5]*V, 0, 0, 0, 0, -k[5]*HY - k[5]*HE, 0],
            # I = +immune + vaccine k[4]*(SY+SE) + k[5]*V*(HY+HE)
            [k[5]*V, 0, k[5]*V, 0, k[4], k[4], 0, k[5]*HY + k[5]*HE, 0]
        ]
        return dfdy
    #print(jacob(0, n))

    nV0 = n[7]
    t1 = np.arange(0, 30, 30/(nMax))
    result1 = integrate.solve_ivp(fun=sick_ode, t_span=(np.min(t1), np.max(t1)), y0=n,
                                  t_eval=t1, method='Radau', jac=jacob)

    t2 = np.arange(30, tSpan, tSpan/(nMax))
    n0 = result1.y[:, -1]
    # print(n0)
    n0[7] += nV0/2
    # print(n0)
    result2 = integrate.solve_ivp(fun=sick_ode, t_span=(np.min(t2), np.max(t2)), y0=n0,
                                  t_eval=t2, method='Radau', jac=jacob)

    # combine values for both time invtervals
    result = [x+y for x, y in zip(result1.y.tolist(), result2.y.tolist())]
    time = result1.t.tolist() + result2.t.tolist()  # combine both time intervals
    return result, time


def get_r(n, k):
    '''
        Helper function for the Gillespie algorithm.
        Gets the relative reaction probabilites.
    '''
    HY, HE, HYF, HEF, SY, SE, D, V, I = n
    r = [
        k[0]*HY*SY,
        k[0]*HY*SE,
        k[0]*HYF*SY,
        k[0]*HYF*SE,
        k[1]*HE*SY,
        k[1]*HE*SE,
        k[1]*HEF*SY,
        k[1]*HEF*SE,
        k[2]*SY,
        k[3]*SE,
        k[4]*SY,
        k[4]*SE,
        k[5]*HY*V,
        k[5]*HE*V
    ]
    return r


def nvsum(n, rxn_num):
    '''
        Helper function, sums the reaction with the current number of items.
        Equations:

        HY + SY -> 2SY          k0= 1.76e-5 day^-1      r0 = k[0]*HY*SY
        HY + SE -> SY + SE                              r1 = k[0]*HY*SE
        HYF + SY -> 2SY                                 r2 = k[0]*HYF*SY
        HYF + SE -> SY + SE                             r3 = k[0]*HYF*SE

        HE + SY -> SY + SE      k1= 0.88e-5 day^-1      r4 = k[1]*HE*SY
        HE + SE -> 2SE                                  r5 = k[1]*HE*SE
        HEF + SY -> SY + SE                             r6 = k[1]*HEF*SY
        HEF + SE -> 2SE                                 r7 = k[1]*HEF*SE

        SY -> D                 k2= 0.010 day^-1        r8 = k[2]*SY
        SE -> D                 k3= 0.030 day^-1        r9 = k[3]*SE

        SY -> I                 k4=?  0.100 day^-1      r10= k[4]*SY
        SE -> I                                         r11= k[4]*SE

        HY + V -> I             k5=?  3.52e-6 day^-1    r12= k[5]*HY*V
        HE + V -> I                                     r13= k[5]*HE*V
    '''
    # n = [HY, HE, HYF, HEF, SY, SE, D, V, I]
    v = np.array((
        [-1, 0, 0, 0, 1, 0, 0, 0, 0],
        [-1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, -1, 0, 1, 0, 0, 0, 0],
        [0, 0, -1, 0, 1, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, 1, 0, 0, 0],
        [0, -1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, -1, 0, 1, 0, 0, 0],
        [0, 0, 0, -1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, -1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, -1, 1, 0, 0],
        [0, 0, 0, 0, -1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, -1, 0, 0, 1],
        [-1, 0, 0, 0, 0, 0, 0, -1, 1],
        [0, -1, 0, 0, 0, 0, 0, -1, 1]
    ))
    n = np.add(n, v[rxn_num])
    return n


def Gillespie_model(n, k, tSpan, nMax):
    ''' 
        Gillespie algorithm allows for a discrete stochastic model
        of the disease. The reactions are converted to probabilites
        and if the reaction occurs, each element is changed relative
        to the reaction and avoiding fractional changes.

        n = [HY, HE, HYF, HEF, SY, SE, D, V, I]
        k = [k0, k1, k2, k3, k4, k5]
    '''
    time = np.zeros(int(nMax))
    t = 0
    result = np.zeros((int(nMax), 9))
    nV0 = n[7]
    last_val = 0
    vacc = True
    for index in range(len(time)):
        if(vacc and t >= 30):
            n[7] += nV0/2  # add new vaccines
            vacc = False

        r = get_r(n, k)  # rxn proportional probabilities
        rtot = sum(r)

        if(rtot == 0 or t >= tSpan):  # stop condition
            last_val = index
            break

        w = np.random.uniform()
        tau = -np.log(w)/rtot  # time step
        result[index] = n
        time[index] = t
        t += tau
        rprob = np.array([i/rtot for i in r])  # rxn probabilities
        csp = np.cumsum(rprob)
        q = np.random.uniform()

        for i, item in enumerate(csp):
            if(q < item):  # if the rand num is less than cumulative prob then the rxn occurs
                rxn_num = i
                n = nvsum(n, rxn_num)
                break

    # stores only results till recorded time index
    res = result.T[:, :last_val]
    # graph(res, time[:last_val]) # graph stochastic
    return res[6, -1]  # deaths


def elba(nY0=(27199, 0, 1), nE0=(4800, 0, 0), nV0=0, timeSpan=120, nMax=2e6, nRun=1):
    '''
        Modeling an epidemic
        nV0 = vaccines t=0
        nV0/2 = vaccines t=30 no more after
        population is 32000, 15% elderly
        nY0 = (HY,HYF,SY) at t=0
        nE0 = (HE,HEF,SE) at t=0

        healthy young = HY
        healthy elderly = HE
        sick young = SY
        sick elderly = SE
        immune = I
        vaccines = V
        healthy young free rider = HYF
        healthy elderly free rider = HEF
        dead = D

        Equations:

        HY + SY -> 2SY          k0= 1.76e-5 day^-1      r0 = k[0]*HY*SY
        HY + SE -> SY + SE                              r1 = k[0]*HY*SE
        HYF + SY -> 2SY                                 r2 = k[0]*HYF*SY
        HYF + SE -> SY + SE                             r3 = k[0]*HYF*SE

        HE + SY -> SY + SE      k1= 0.88e-5 day^-1      r4 = k[1]*HE*SY
        HE + SE -> 2SE                                  r5 = k[1]*HE*SE
        HEF + SY -> SY + SE                             r6 = k[1]*HEF*SY
        HEF + SE -> 2SE                                 r7 = k[1]*HEF*SE

        SY -> D                 k2= 0.010 day^-1        r8 = k[2]*SY
        SE -> D                 k3= 0.030 day^-1        r9 = k[3]*SE

        SY -> I                 k4=?  0.100 day^-1      r10= k[4]*SY
        SE -> I                                         r11= k[4]*SE

        HY + V -> I             k5=?  3.52e-6 day^-1    r12= k[5]*HY*V
        HE + V -> I                                     r13= k[5]*HE*V

        do model from t=0-30 then use results as initial conditions for next

        variables n = [HY, HYF, HE, HEF, SY, SE, D, V, I]
        rate const k = [k0, k1, k2, k3, k4, k5]

    '''
    # input error checking
    if (nRun < 1):
        raise Exception('nRun must be greater than or equal to 1')
    if(sum(nY0)+sum(nE0) != TOTAL_POPULATION):
        raise Exception(
            'nY0 and nE0 must be tuples that add up to the total population:', TOTAL_POPULATION)
    if (sum(nY0) != 0.85*TOTAL_POPULATION):
        raise Exception('Young folks should be 85% of the total population')
    if (sum(nE0) != 0.15*TOTAL_POPULATION):
        raise Exception('Elderly folks should be 15% of the total population')

    HY0, HYF0, SY0 = nY0
    HE0, HEF0, SE0 = nE0
    D0, V0, I0 = 0, nV0, 0
    n0 = (HY0, HYF0, HE0, HEF0, SY0, SE0, D0, V0, I0)  # inital conditions
    k = [1.76e-5, 0.88e-5, 0.010, 0.030, 0.100, 3.52e-6]  # day^-1 rate consts

    ode_result, time = ode_model(n=n0, k=k, tSpan=timeSpan, nMax=nMax)

    gil_deaths = np.zeros(nRun)
    for i in range(nRun):
        gil_deaths[i] = Gillespie_model(n=n0, k=k, tSpan=timeSpan, nMax=nMax)

    graph(ode_result, time, gil_deaths)

    return


def graph(result, time, gil_deaths=0):
    '''
        Plots the results side by side. The deterministic model
        is on the left and shows the number of items over time
        and the stochastic model is on the right showing the
        number of deaths per run.
    '''
    HY, HE, HYF, HEF, SY, SE, D, V, I = result
    # print('deaths:', D[-1])
    t = time
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.plot(t, I, t, np.add(HYF, HY), t, np.add(HEF, HEF), t, SY, t, SE, t, D)
    ax1.set(ylim=(0, 35000), xlim=(0, time[-1]), xlabel='time (days)',
            ylabel='number of people',
            title='Elba Epidemic: Continuous-variable, deterministic model')
    labels = ('I', 'HYF+HY', 'HEF+HE', 'SY', 'SE', 'D')
    ax1.legend(labels, loc='upper right')
    s = ('deaths:' + str(int(D[-1])))
    ax1.text(0.2, 0.9, s, ha='center', va='center', transform=ax1.transAxes)
    ax2.hist(gil_deaths)
    ax2.set(xlabel='number of deaths',
            ylabel=('number of runs (out of ' + str(len(gil_deaths)) + ' total)'),
            title='Elba Epidemic: Discrete-variable, stochastic model')
    plt.show()


if __name__ == '__main__':
    # v = TOTAL_POPULATION*0.30
    # y = 27199
    # e = 4800
    # p = 0.15  # prob free rider
    # ef, eh = int(v*p), e-int(v*p)
    # yf, yh = int(v*(1-p)), y-int(v*(1-p))

    # yf, ef = int(p*y), int(p*e)
    # yh, eh = y - yf, e - ef
    # elba(nY0=(27200, 0, 0), nE0=(798, 4000, 2), nV0=15000, timeSpan=120, nMax=2e6, nRun=10)
    # elba(nY0=(27199, 0, 1), nE0=(4800, 0, 0), nV0=15000, timeSpan=120, nMax=2e6, nRun=1) # o FR
    # elba(nY0=(yh, yf, 1), nE0=(4800, 0, 0), nV0=15000, timeSpan=120, nMax=2e6, nRun=10) # yf%
    # elba(nY0=(yh, yf, 1), nE0=(eh, ef, 0), nV0=15000, timeSpan=120, nMax=2e6, nRun=50) # ef%
    # elba(nY0=(yh, yf, 1), nE0=(eh, ef, 0),
    #      nV0=20000, timeSpan=120, nMax=2e6, nRun=10)
    # elba(nY0=(27200, 0, 0), nE0=(4800-4002, 4000, 2), nV0=15000, timeSpan=120, nMax=2e6, nRun=50)
    elba(nY0=(27199-20000, 20000, 1), nE0=(4800, 0, 0),
         nV0=5000, timeSpan=120, nMax=2e6, nRun=10)
    pass
