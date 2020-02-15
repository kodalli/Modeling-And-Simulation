'''
    Hydrogen fuel cell calculations and graph generation
    Created by: Surya Kodali
'''

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

file_name = r'HFC_copy.xlsx'
sheet = 'cs1'
df = pd.read_excel(file_name, sheet_name=sheet)
# Nitrogen Flowrate (mL/min)	MFM2	Hydrogen Flowrate (mL/min)	Resistance (Ohms)	Current (A)	Voltage (V)	Fuel Cells
n_flow = list(df.iloc[:,0])

h_flow = list(df.iloc[:,2])
Resistance = list(df.iloc[:,3])
Current = list(df.iloc[:,4])
Voltage = list(df.iloc[:,5])
Num_Fuel_Cells = df.iloc[0,6]

print(Num_Fuel_Cells)