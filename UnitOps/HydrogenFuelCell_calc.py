'''
    Hydrogen fuel cell calculations and graph generation
    Created by: Surya Kodali
'''

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

file_name = r'HFC_copy.xlsx'
# all 150 mL nitrogen flow rate
nine_fuel_cell = 'cs1'
seven_fuel_cell = 'cs2'
five_fuel_cell = 'cs3-150'
three_fuel_cell = 'cs4-150'

df3 = pd.read_excel(file_name, sheet_name=three_fuel_cell)
df5 = pd.read_excel(file_name, sheet_name=five_fuel_cell)
df7 = pd.read_excel(file_name, sheet_name=seven_fuel_cell)
df9 = pd.read_excel(file_name, sheet_name=nine_fuel_cell)
# Nitrogen Flowrate (mL/min)	MFM2	Hydrogen Flowrate (mL/min)	Resistance (Ohms)	Current (A)	Voltage (V)	Fuel Cells


def loadData(df):
    n_flow = list(df.iloc[:, 0])
    h_flow = list(df.iloc[:, 2])
    Resistance = list(df.iloc[:, 3])
    Current = list(df.iloc[:, 4])
    Voltage = list(df.iloc[:, 5])
    Num_Fuel_Cells = df.iloc[0, 6]
    h_conc = []
    for h, n in zip(h_flow, n_flow):
        h_conc.append(h/n)
    return (n_flow, h_flow, Resistance, Current, Voltage, Num_Fuel_Cells, h_conc)


def graph_volt_conc(p, color):
    conc, voltage, resistance, num_cells = p[6], p[4], p[2], p[5]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(conc, voltage, resistance, c=color, marker='o')
    ax.set_xlabel('Hydrogen Conc. (H2/N2)')
    ax.set_ylabel('Voltage (V)')
    ax.set_zlabel('Resistance (Ohms)')
    title = 'Voltage vs Hydrogen Concentration for ' + \
        str(num_cells) + ' Fuel Cells'
    ax.set_title(title)
    plt.show()


def graph_current_conc(p, color):
    conc, current, resistance, num_cells = p[6], p[3], p[2], p[5]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(conc, current, resistance, c=color, marker='o')
    ax.set_xlabel('Hydrogen Conc. (H2/N2)')
    ax.set_ylabel('Current (Amperes)')
    ax.set_zlabel('Resistance (Ohms)')
    title = 'Current vs Hydrogen Concentration for ' + \
        str(num_cells) + ' Fuel Cells'
    ax.set_title(title)
    plt.show()


def graph_volt_all(p3, p5, p7, p9):
    fig = plt.figure()
    c3, v3, r3, n3 = p3[6], p3[4], p3[2], p3[5]
    c5, v5, r5, n5 = p5[6], p5[4], p5[2], p5[5]
    c7, v7, r7, n7 = p7[6], p7[4], p7[2], p7[5]
    c9, v9, r9, n9 = p9[6], p9[4], p9[2], p9[5]
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(c3, v3, r3, c='r', marker='o', label=str(n3) + ' Fuel Cells')
    ax.scatter(c5, v5, r5, c='b', marker='o', label=str(n5) + ' Fuel Cells')
    ax.scatter(c7, v7, r7, c='g', marker='o', label=str(n7) + ' Fuel Cells')
    ax.scatter(c9, v9, r9, c='m', marker='o', label=str(n9) + ' Fuel Cells')
    ax.set_xlabel('Hydrogen Conc. (H2/N2)')
    ax.set_ylabel('Voltage (V)')
    ax.set_zlabel('Resistance (Ohms)')
    title = 'Voltage vs Hydrogen Concentration for Fuel Cells'
    ax.set_title(title)
    ax.legend()
    plt.show()


def farady_efficiency(p):
    fconst = 96485.33  # C/mol
    current, h_flow, num_cells, resistance = p[3], p[1], p[5], p[2]
    mol_hydrogen = []
    for h in h_flow:
        mol_hydrogen.append(0.136092 * float(h) /
                            (1000 * 0.0820574 * 293 * 60))  # n = PV/RT
    print(mol_hydrogen)
    print(current)
    theoretical_current = []
    for m in mol_hydrogen:
        theoretical_current.append(2 * m * fconst)
    print(theoretical_current)
    f_eff = []
    for exp, theor in zip(current, theoretical_current):
        if(theor != 0):
            f_eff.append(exp/theor)
        elif(theor == 0):
            f_eff.append(0)
    print(f_eff)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(h_flow, f_eff, resistance, c='r', marker='o')
    ax.set_xlabel('Hydrogen Flow (mL/min)')
    ax.set_ylabel('Faraday Efficiency')
    ax.set_zlabel('Resistance (Ohms)')
    title = 'Faraday Efficiency vs Hydrogen Flow Rate for ' + \
        str(num_cells) + ' Fuel Cells'
    ax.set_title(title)
    plt.show()


if __name__ == "__main__":
    p3 = loadData(
        df3)

    p5 = loadData(
        df5)

    p7 = loadData(
        df7)

    p9 = loadData(
        df9)

    # graph_volt_conc(p3, 'r')
    # graph_volt_conc(p5, 'b')
    # graph_volt_conc(p7, 'c')
    # graph_volt_conc(p9, 'm')

    # graph_current_conc(p3, 'r')
    # graph_current_conc(p5, 'b')
    # graph_current_conc(p7, 'c')
    # graph_current_conc(p9, 'm')

    # graph_volt_all(p3, p5, p7, p9)

    farady_efficiency(p3)

    pass
