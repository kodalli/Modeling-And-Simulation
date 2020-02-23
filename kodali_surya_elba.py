import numpy as np 
import matplotlib.pyplot as plt 

TOTAL_POPULATION = 32000

def ode_model():
    return


def Gillespie_model():
    return


def elba(nY0=(27199,0,0), nE0=(4800,0,0), nV0=0, timeSpan=120, nMax=2e6, nRun=1):
    '''
        Modeling an epidemic
        nV0 = vaccines t=0
        nV0/2 = vaccines t=30 no more after
        population is 32000, 15% elderly
        
        HY + SY -> 2SY          k1= 0.88e-5 day^-1
        HY + SE -> SY + SE      k1
        HE + SY -> SY + SE      k2= 1.76e-5 day^-1
        HE + SE -> 2SE          k2  
        
        SE -> DE                k3= 0.010 day^-1
        SY -> DY                k4= 0.030 day^-1
        
        (SE + SY) -> I          k5=
        
        (HE + HY) + V -> I      k6=
        
        do model from t=0-30 then use results as initial conditions for next
    '''
    if (nRun < 1):
        raise Exception('nRun must be greater than or equal to 1')
    return
    if(np.sum(nY0, nE0) != TOTAL_POPULATION):
        raise Exception('nY0 and nE0 must add up to the total population:', TOTAL_POPULATION)
    return

if __name__ == '__main__':
    pass