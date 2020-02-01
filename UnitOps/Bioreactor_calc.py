import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.optimize import fsolve
from scipy.optimize import curve_fit

root = r'C:\Users\Surya\Documents\Python Scripts\CBE\UnitOps'
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

for i in range(len(time)):
    dilution_factor[i] = (volume_cells[i] +
                          volume_water[i]) / volume_cells[i]
    optical_density[i] = spec[i] * dilution_factor[i]
    mass_concentration[i] = optical_density[i]*(3e7)*(2e-12)*1000
print('dilution factor:', dilution_factor)
print('optical density:', optical_density)

exp_pt = 2

# plt.scatter(time[exp_pt:-4], np.log(optical_density[exp_pt:-4]))
# plt.show()

res = linregress(time[exp_pt:-4], np.log(optical_density[exp_pt:-4]))
print(res)
slope = res[0]
td = np.log(2) / slope
print('slope =', slope, 'hrs^-1', 'td =', td, 'hrs')
print('mass conc:', mass_concentration)

# plt.scatter(time, np.log(optical_density))
# plt.title(flask)
# plt.xlabel('Time (hrs)')
# #plt.ylabel('Actual OD')
# plt.ylabel('log(Actual OD)')

i = 0

tempx = []
while(i < time[-4]):
    tempx.append(time[exp_pt]+i)
    i+=0.1

tempy = []
for i, item in enumerate(tempx):
    tempy.append(slope*item + res[1])

# plt.plot(tempx, tempy)
# plt.show()

desired_slope = 0.012
def eqn(p):
    S = p
    Xo = mass_concentration[0]
    X = mass_concentration[-1]
    So = glucose_concentration[0]
    return(
        (X-Xo)/(So-S) - desired_slope
    )


S = fsolve(eqn, (1))
print('S = ', S)

def func(x, a, b):
    return a*np.exp(b*x)

popt, pcov = curve_fit(func, time, mass_concentration, p0=(0.5, 1e-6))
a = popt[0]
b = popt[1]
print(a,'*exp(',b,'*t)')
c = a*b
um = c*np.exp(b*time[-1])
print('um =', um)
u_star = um/2
print('u* =', u_star)
t_star = 1/b * np.log(u_star/c)
print('t* =', t_star)
x_star = a*np.exp(b*t_star)
print('x_star =', x_star)
S_star = glucose_concentration[0] - (x_star-mass_concentration[0])/desired_slope
print('S_star =', S_star)

plt.scatter(time, mass_concentration, zorder = 1)
plt.xlabel('Time (hrs)')
plt.ylabel('Cell Mass Conc. (g/L)')
plt.title(flask)
plt.grid(zorder = -1)
i = 0
x = []
while(i < time[-1]):
    x.append(time[0]+i)
    i+=0.1

y = []
for item in x:
    y.append(a*np.exp(item*b))

plt.plot(x, y)

plt.show()