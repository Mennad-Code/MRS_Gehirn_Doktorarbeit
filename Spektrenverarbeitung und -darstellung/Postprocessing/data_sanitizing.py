import numpy as np
import pandas as pd

# konstante Variablen
from Variables.constants import *

# isoliere den Realteil der Spektren
def real(df_spec):
    df_spec = df_spec.map(np.real)
    return df_spec

# Funktion zur Index-Auswahl der Spektren nach den Kriterien Alterskategorie, Voxelposition und Diagnose
def spec_selec(df_befund,df_spec,alter_categ=None,vp=None,diag=None,diag_categ=None):
    index = df_befund.index
    temp = index.isin(df_spec.index)
    index = index[temp]
    if alter_categ:
        index = df_befund.loc[index]['Alterskategorie']==alter_categ
        index = index[index].index
    if vp:
        index = df_befund.loc[index][('Voxelposition','')]==vp
        index = index[index].index
    if diag:
        index = df_befund.loc[index][('Befund','')]==diag
        index = index[index].index
    if diag_categ:
        index = df_befund.loc[index][('Diagnosekategorie','')]==diag_categ
        index = index[index].index
    return index

# mit Vorauswahl der IDs und der Möglichkeit nach mehreren Diagnosen zu filtern
def spec_selec_preselec(df_befund,df_spec,alter_categ=None,vp=None,diag=None,diag_categ=None, index=None):
    if not index.empty:
        index = df_befund.index
    else:
        temp = index.isin(df_spec.index)
        index = index[temp]
        
    if alter_categ:
        index = df_befund.loc[index]['Alterskategorie']==alter_categ
        index = index[index].index
    if vp:
        index = df_befund.loc[index][('Voxelposition','')]==vp
        index = index[index].index
    if diag:
        if isinstance(diag,list):
            index = df_befund.loc[index]['Befund'].isin(diag)
            index = index[index].index
        else:
            index = df_befund.loc[index][('Befund','')]==diag
            index = index[index].index
    if diag_categ:
        index = df_befund.loc[index][('Diagnosekategorie','')]==diag_categ
        index = index[index].index
    return index

# Funktion zur Index-Auswahl der Spektren nach den Kriterien Alterskategorie, Voxelposition und Diagnose: nimmt ganze Datensätze als Argumente an
def spec_selec_dataset(ds,alter_categ=None,vp=None,diag=None,diag_categ=None,i=1,excluded=False):
    df_befund,df_spec,_,_,_ = ds.dataset.load_dataset(i)

    if(not excluded):
        index = df_befund.index
        temp = index.isin(df_spec.index)
        index = index[temp]
    else:
        index = df_befund.index
        temp = index.isin(df_spec.index)
        index = index[~temp]
    
    if alter_categ:
        index = df_befund.loc[index]['Alterskategorie']==alter_categ
        index = index[index].index
    if vp:
        index = df_befund.loc[index][('Voxelposition','')]==vp
        index = index[index].index
    if diag:
        index = df_befund.loc[index][('Befund','')]==diag
        index = index[index].index
    if diag_categ:
        index = df_befund.loc[index][('Diagnosekategorie','')]==diag_categ
        index = index[index].index

    return index

# entferne alle irrelevanten Voxelpositionen
def entferne_irr_vp(df_befund,index):
    return index[df_befund['Voxelposition'].loc[index].isin(['Basalganglien','Marklager'])]

# entferne Diagnosekategorie 'Nicht bekannt'
def entferne_nbekannt(ds,i,index):
    df_befund,_,_,_,_ = ds.dataset.load_dataset(i)
    index_temp = df_befund['Diagnosekategorie'].loc[index]!='Nicht bekannt'
    index_temp = index_temp[index_temp].index
    return index_temp

# Wähle die entsprechenden Altersgruppen
def waehle_altersgruppen(df_befund,index):
    alter_gr_selec = []
    for alter_gr in ALTERSGRUPPE_NAMEN:
        if alter_gr in df_befund['Alterskategorie'].loc[index].unique():
            alter_gr_selec.append(alter_gr)
    return alter_gr_selec

# Richtige Formattierung der Dataframes fürs Plotten, sowie die Auswahl durch den Index
def process_specs(df_befund,df_spec,df_chemshift,index_selec):
    a = pd.melt(df_chemshift.loc[index_selec].join(df_befund["Farbton"].loc[index_selec]).reset_index(), id_vars=['index','Farbton'], var_name='variable', value_name='x')
    b = pd.melt(df_spec.loc[index_selec].join(df_befund["Farbton"].loc[index_selec]).reset_index(), id_vars=['index','Farbton'], var_name='variable', value_name='y')
    spec_plottable = pd.merge(a, b, on=['index','variable','Farbton']).drop(columns=['variable'])
    return spec_plottable

# formatiere die Spektren-Dataframes so, dass sie mit unterschiedlichen ppm-Werten geplottet werden können
def format_df4plot(df_spec,df_chemshift,index_selec):
    # index ist hier in Echt nach .reset_index() die Spektren-ID
    x_values = pd.melt(df_chemshift.loc[index_selec].reset_index(),id_vars=['index'],var_name='arr_index',value_name='x')
    y_values = pd.melt(df_spec.loc[index_selec].reset_index(),id_vars=['index'],var_name='arr_index',value_name='y')
    spec_plottable = pd.merge(x_values, y_values, on=['index','arr_index']).drop(columns=['arr_index'])
    return spec_plottable

# Isoliere den signifikanten Wert (ungleich 0) der Altersgrenzen, wichtig für die Erstellung der Colorbars für die farbkodierte Darstellung
def isolate_signifcant_digit(arr):
    if arr[arr.astype(bool)]:
        return arr[arr.astype(bool)]
    else:
        return 0
    
