import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.optimize import fsolve
from scipy.optimize import curve_fit

root = r'G:\PyScripts\CBE\CBE\UnitOps'
name = r'BR_all_data_copy.xlsx'
file_name = os.path.join(root, name)
flask = 'flask4'
df = pd.read_excel(file_name, sheet_name=flask)
# print(df)
# print(df.iloc[0])  # gives first row
# print(list(df.iloc[0])) # first row of values
# print(df.iloc[:, 0]) first column of values

time = list(df.iloc[:, 0])
volume_cells = list(df.iloc[:, 1])
volume_water = list(df.iloc[:, 2])
dilution_factor = list(df.iloc[:, 3])
spec = list(df.iloc[:, 4])
optical_density = list(df.iloc[:, 5])
mass_concentration = list(df.iloc[:, 6])
glucose_concentration = list(df.iloc[:, 7])

# print(mass_concentration)
# Calculatioins for empty columns in excel sheet
for i in range(len(time)):
    dilution_factor[i] = (volume_cells[i] +
                          volume_water[i]) / volume_cells[i]
    optical_density[i] = spec[i] * dilution_factor[i]
    mass_concentration[i] = optical_density[i]*(3e7)*(2e-12)*1000
# print('dilution factor:', dilution_factor)
# print('optical density:', optical_density)


# plt.scatter(time[exp_pt:-4], np.log(optical_density[exp_pt:-4]))
# plt.show()
# Linear regression slope from range, also td, and mass conc
exp_pt = 1
res = linregress(time[exp_pt:7], np.log(optical_density[exp_pt:7]))
print(res)
slope = res[0]
td = np.log(2) / slope
print('slope =', slope, 'hrs^-1', 'td =', td, 'hrs')
# print('mass conc:', mass_concentration)


# generates points for linreg line to plot
i = 0
tempx = []
while(i < time[-4]):
    tempx.append(time[exp_pt]+i)
    i += 0.1
tempy = []
for item in tempx:
    tempy.append(slope*item + res[1])

# plt.plot(tempx, tempy)
# plt.show()

desired_slope = 0.012  # yeild factor chosen
Xo = mass_concentration[0]
X = mass_concentration[-1]
So = glucose_concentration[0]


def eqn(p):
    S = p
    return(
        (X-Xo)/(So-S) - desired_slope
    )


S = fsolve(eqn, (1))
print('S = ', S)  # final substrate concentration


# exponential curve fit
def func(x, a, b):
    return a*np.exp(b*x)


popt, pcov = curve_fit(
    func, time[:-3], mass_concentration[:-3], p0=(0.5, 1e-6))
a = popt[0]  # estimate coefficients
b = popt[1]
print(a, '* exp(', b, '*t )')
c = a*b
# slope of um is the last point of the exponential phase
um = c*np.exp(b*time[-1])
print('um =', um)
u_star = um/2
print('u* =', u_star)
t_star = 1/b * np.log(u_star/c)
print('t* =', t_star)
x_star = a*np.exp(b*t_star)
print('x* =', x_star)
S_star = glucose_concentration[0] - \
    (x_star-mass_concentration[0])/desired_slope
print('S* =', S_star)
Ks = S_star
Yxs = desired_slope


# Michaelis-Menten
def mm(p):
    X = p
    return (
        (Ks*Yxs + So*Yxs + Xo)/(Yxs*So + Xo) * np.log(X/Xo) - (Yxs*So) /
        (Yxs*So + Xo) * np.log((Yxs*So + Xo - X)/(Yxs*So)) - um*t
    )


t = 0
mmList = []
for i in time:
    t = i
    temp = fsolve(mm, (0.01))
    mmList.append(float(temp))


def printVals():
    print('dilution factor:')
    for x in range(len(dilution_factor)):
        print(dilution_factor[x])
    print('optical density:')
    for x in range(len(optical_density)):
        print(optical_density[x])
    print('mass concentration:')
    for x in range(len(mass_concentration)):
        print(mass_concentration[x])


def plotLogOD():
    res = linregress(time[1:-3], np.log(optical_density[1:-3]))
    slope, intercept = res[0], res[1]

    i = 0
    x = []
    while(i+time[1] < time[-4]):
        x.append(time[1]+i)
        i += 0.01

    y = []
    for item in x:
        y.append(slope * item + intercept)
    fig, ax = plt.subplots(1)
    ax.plot(x, y)
    ax.scatter(time[1:-3], np.log(optical_density[1:-3]))
    # ax.set_title(flask)
    ax.set_xlabel('Time (hrs)')
    ax.set_ylabel('log(OD600)')
    # ax.set_ylim(ymin=0)
    # ax.set_xlim(xmin=-0.1)
    ax.set_axisbelow(True)
    plt.grid()
    plt.show(fig)


def plotOD():
    fig, ax = plt.subplots(1)
    ax.scatter(time, optical_density)
    # ax.set_title(flask)
    ax.set_xlabel('Time (hrs)')
    ax.set_ylabel('OD600')
    # ax.set_ylim(ymin=0)
    # ax.set_xlim(xmin=-0.1)
    ax.set_axisbelow(True)
    plt.grid()
    plt.show(fig)


def plotMassConc():
    fig, ax = plt.subplots(1)
    ax.scatter(time, mass_concentration)
    ax.set_xlabel('Time (hrs)')
    ax.set_ylabel('Cell Mass Conc. (g/L)')
    # ax.set_title(flask)
    # exponential curve plot
    i = 0
    x = []
    while(i+time[0] < time[-1]):
        x.append(time[0]+i)
        i += 0.01

    y = []
    for item in x:
        y.append(a*np.exp(item*b))

    ax.plot(x, y)
    # ax.set_ylim(ymin=0)
    # ax.set_xlim(xmin=-0.1)
    ax.set_axisbelow(True)
    plt.grid()
    plt.show(fig)


def plotMichaelis():
    fig, ax = plt.subplots(1)
    ax.scatter(time, mass_concentration)
    ax.scatter(time, mmList)
    ax.set_xlabel('Time (hrs)')
    ax.set_ylabel('Cell Mass Conc. (g/L)')
    # ax.set_title(flask)
    ax.set_axisbelow(True)
    plt.grid()
    plt.show(fig)


if __name__ == "__main__":
    plotOD()
    plotLogOD()
    plotMassConc()
    plotMichaelis()
    # printVals()
