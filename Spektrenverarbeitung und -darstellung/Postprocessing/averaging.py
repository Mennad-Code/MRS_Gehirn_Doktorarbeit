import numpy as np
import pandas as pd

import scipy as sci

from Postprocessing.math_funcs import ceil_to_first_sign_dig

def new_x_values(df_chemshift):
    #bestimme den maximalen und den minimalen Wert des Chemical Shifts
    minmax = df_chemshift.min(axis=1).max()
    maxmin = df_chemshift.max(axis=1).min()
    # die Auflösung des Durchschnitts nach dem Chemical Shift darf höchstens so hoch sein, wie die schlechteste Aufläsung unter den Chemical-Shift-Skalen
    min_stepsize = df_chemshift.diff(axis=1).loc[:,1].max()
    min_stepsize = ceil_to_first_sign_dig(min_stepsize)
    # Anzahl der zu interpolierenden Datenpunkte
    data_point_num = np.floor((maxmin-minmax)/min_stepsize).astype(int)
    return np.linspace(minmax,maxmin,num=data_point_num)

def interpoliere_spektren(df_spec,df_chemshift,new_x_values):
    # Erstelle die linear interpolierte kontinuierliche Funktion
    interpol_funcs = df_spec.apply(lambda y: sci.interpolate.interp1d(df_chemshift.loc[y.name],y),axis=1)
    # Erstelle alle neuen x-Werte damit und füge die x-Werte als Spalten hinzu
    df_spec_new = df_spec.apply(lambda x: interpol_funcs[x.name](new_x_values),axis=1,result_type='expand')
    df_spec_new.columns = new_x_values
    return df_spec_new