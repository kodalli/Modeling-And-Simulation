import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import random as rand
import pandas as pd

TOTAL_POPULATION = 32000


def ode_model(n, k, tSpan, nMax):
    '''
        n = [HY, HE, HYF, HEF, SY, SE, D, V, I]
        k = [k0, k1, k2, k3, k4, k5]
    '''
    def sick_ode(t, n):
        HY, HYF, HE, HEF, SY, SE, D, V, I = n
        dndt = np.array((
            #HY = -sick -vaccine
            -k[0]*HY*(SY+SE) -k[5]*HY*V,
            #HYF = -sick 
            -k[0]*HYF*(SY+SE),
            #HE = -sick -vaccine
            -k[1]*HE*(SY+SE) -k[5]*HE*V,
            #HEF = -sick 
            -k[1]*HEF*(SY+SE),
            #SY = +sick - dead - immune
            k[0]*HY*(SY+SE) + k[0]*HYF*(SY+SE) -k[2]*SY -k[4]*(SY+SE),
            #SE = +sick - dead - immune
            k[1]*HE*(SY+SE) + k[1]*HEF*(SY+SE) -k[3]*SE -k[4]*(SY+SE),
            #D = +dead
            k[2]*SY + k[3]*SE,
            #V = -vaccine
            -k[5]*V*(HY+HE),
            #I = +immune + vaccine
            k[4]*(SY+SE) + k[5]*V*(HY+HE)
        ))
        return dndt
    
    def jacob(t, n):
        HY, HYF, HE, HEF, SY, SE, D, V, I = n
        dfdy = np.array((
            #HY = -sick -vaccine -k[0]*HY*(SY+SE) -k[5]*HY*V
            [-k[0]*(SY+SE) -k[5]*V, 0, 0, 0, -k[0]*HY, -k[0]*HY, 0, -k[5]*HY, 0],
            #HYF = -sick -k[0]*HYF*(SY+SE)
            [0, -k[0]*(SY+SE), 0, 0, -k[0]*HYF, -k[0]*HYF, 0, 0, 0],
            #HE = -sick -vaccine -k[1]*HE*(SY+SE) -k[5]*HE*V
            [0, 0, -k[1]*(SY+SE) -k[5]*V, 0, -k[1]*HE, -k[1]*HE, 0, -k[5]*HE, 0],
            #HEF = -sick -k[1]*HEF*(SY+SE)
            [0, 0, 0, -k[1]*(SY+SE), -k[1]*HEF, -k[1]*HEF, 0, 0, 0],
            #SY = +sick - dead k[0]*HY*(SY+SE) + k[0]*HYF*(SY+SE) -k[2]*SY -k[4]*(SY+SE)
            [k[0]*(SY+SE), k[0]*(SY+SE), 0, 0, k[0]*HY + k[0]*HYF -k[2] -k[4], k[0]*HY + k[0]*HYF -k[4], 0, 0, 0],
            #SE = +sick - dead k[1]*HE*(SY+SE) + k[1]*HEF*(SY+SE) -k[3]*SE -k[4]*(SY+SE)
            [0, 0, k[1]*(SY+SE), k[1]*(SY+SE), k[1]*HE + k[1]*HEF -k[4], k[1]*HE + k[1]*HEF -k[3] -k[4], 0, 0, 0],
            #D = +dead k[2]*SY + k[3]*SE
            [0, 0, 0, 0, k[2], k[3], 0, 0, 0],
            #V = -vaccine -k[5]*V*(HY+HE)
            [-k[5]*V, 0, -k[5]*V, 0, 0, 0, 0, -k[5]*(HY+HE), 0],
            #I = +immune + vaccine k[4]*(SY+SE) + k[5]*V*(HY+HE)
            [k[5]*V, 0, k[5]*V, 0, k[4], k[4], 0, k[5]*(HY+HE), 0]
        ))
        return dfdy
    
    nV0 = n[7]
    t1 = np.arange(0,30,30/(nMax))
    result1 = integrate.solve_ivp(fun=sick_ode, t_span=(0,30), y0=n,
                               t_eval=t1, method='Radau', jacob=jacob)
    
    t2 = np.arange(30,tSpan,tSpan/(nMax))
    n_res = result1.y 
    n0 = [n_res[x][-1] for x in range(len(n_res))]
    n0[7] += nV0/2
    result2 = integrate.solve_ivp(fun=sick_ode, t_span=(30,tSpan), y0=n0,
                               t_eval=t2, method='Radau', jacob=jacob)
    print(result1.y.shape)
    print(result2.y.shape)
    result = [x+y for x,y in zip(result1.y.tolist(), result2.y.tolist())]
    time = result1.t.tolist() + result2.t.tolist()
    return result, time

def get_r(n, k):
    HY, HE, HYF, HEF, SY, SE, D, V, I = n
    r = np.array((
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
    ))
    return r

def nvsum(n, rxn_num):
    '''
        Equations:

        HY + SY -> 2SY          k0= 0.88e-5 day^-1      r0 = k[0]*HY*SY
        HY + SE -> SY + SE                              r1 = k[0]*HY*SE
        HYF + SY -> 2SY                                 r2 = k[0]*HYF*SY
        HYF + SE -> SY + SE                             r3 = k[0]*HYF*SE

        HE + SY -> SY + SE      k1= 1.76e-5 day^-1      r4 = k[1]*HE*SY
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
        n = [HY, HE, HYF, HEF, SY, SE, D, V, I]
        k = [k0, k1, k2, k3, k4, k5]
    '''
    time = np.zeros(int(nMax))
    t = 0
    result = []
    for index, _ in enumerate(time):
        r = get_r(n, k)
        rtot = sum(r)
        if(rtot == 0):
            break
        w = rand.random()
        tau = np.log(w)/rtot
        result.append(n)
        time[index] = t
        t+=tau
        rprob = [i/rtot for i in r]
        csp = pd.Series(rprob).cumsum()
        q = rand.random()
        rxn_num = 0
        for i, item in enumerate(csp):
            if(q < item):
                rxn_num = i
                break
        n = nvsum(n, rxn_num)
    result = np.array(result)
    print(result.shape)
    return result.T, time


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

        HY + SY -> 2SY          k0= 0.88e-5 day^-1      r0 = k[0]*HY*SY
        HY + SE -> SY + SE                              r1 = k[0]*HY*SE
        HYF + SY -> 2SY                                 r2 = k[0]*HYF*SY
        HYF + SE -> SY + SE                             r3 = k[0]*HYF*SE

        HE + SY -> SY + SE      k1= 1.76e-5 day^-1      r4 = k[1]*HE*SY
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
    if (nRun < 1):
        raise Exception('nRun must be greater than or equal to 1')
    if(sum(nY0)+sum(nE0) != TOTAL_POPULATION):
        raise Exception(
            'nY0 and nE0 must add up to the total population:', TOTAL_POPULATION)
    if (sum(nY0) != 0.85*TOTAL_POPULATION):
        raise Exception('Young folks should be 85% of the total population')
    if (sum(nE0) != 0.15*TOTAL_POPULATION):
        raise Exception('Elderly folks should be 15% of the total population')
    

    HY0, HYF0, SY0 = nY0
    HE0, HEF0, SE0 = nE0
    D0, V0, I0 = 0, nV0, 0
    n0 = (HY0, HYF0, HE0, HEF0, SY0, SE0, D0, V0, I0)
    k = [0.88e-5, 1.76e-5, 0.010, 0.030, 0.100, 3.52e-6] # day^-1
    
    # ode_result, time = ode_model(n=n0, k=k, tSpan=timeSpan, nMax=nMax)
    # print(np.array(ode_result[6]))
    # graph(ode_result, time)
    
    gil_result, time = Gillespie_model(n=n0, k=k, tSpan=timeSpan, nMax=nMax)
    graph(gil_result, time)
    
    return

def graph(result, time):
    HY, HE, HYF, HEF, SY, SE, D, V, I = result
    t = time
    fig, ax1 = plt.subplots(1,1)
    ax1.plot(t, I, t, V)
    #ax2.plot(t, V)
    plt.show()

if __name__ == '__main__':
    elba(nY0=(27200, 0, 0), nE0=(798, 4000, 2), nV0=15000, timeSpan=120, nMax=2e6, nRun=1)
    pass
