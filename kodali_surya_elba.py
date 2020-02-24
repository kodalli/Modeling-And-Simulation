import numpy as np
import matplotlib.pyplot as plt

TOTAL_POPULATION = 32000


def ode_model():
    return


def Gillespie_model():
    return


def elba(nY0=(27199, 0, 0), nE0=(4800, 0, 0), nV0=0, timeSpan=120, nMax=2e6, nRun=1):
    '''
        Modeling an epidemic
        nV0 = vaccines t=0
        nV0/2 = vaccines t=30 no more after
        population is 32000, 15% elderly

        healthy young = HY
        healthy elderly = HE
        sick young = SY
        sick elderly = SE
        immune = I
        vaccines = V
        healthy young free rider = HYF
        healthy elderly free rider = HEF
        dead = D

        variables = [HY, HE, HYF, HEF, SY, SE, D, V, I]

        Equations:

        HY + SY -> 2SY          k1= 0.88e-5 day^-1      r1 = k1*(HY*(SY+SE) + HYF*(SY+SE))
        HY + SE -> SY + SE
        HYF + SY -> 2SY
        HYF + SE -> SY + SE

        HE + SY -> SY + SE      k2= 1.76e-5 day^-1      r2 = k2*HE*(SY+SE)
        HE + SE -> 2SE            
        HEF + SY -> SY + SE
        HEF + SE -> 2SE



        SE -> D                 k3= 0.010 day^-1        r3 = k3*SE
        SY -> D                 k4= 0.030 day^-1        r4 = k4*SY

        SY -> I                 k5=?                    r5 = k5*(SY+SE)
        SE -> I                 

        HY + V -> I             k6=?                    r6 = k6*V*(HY+HE)
        HE + V -> I             

        do model from t=0-30 then use results as initial conditions for next


    '''
    if (nRun < 1):
        raise Exception('nRun must be greater than or equal to 1')
    if(np.sum(nY0, nE0) != TOTAL_POPULATION):
        raise Exception(
            'nY0 and nE0 must add up to the total population:', TOTAL_POPULATION)
    return


if __name__ == '__main__':
    pass
