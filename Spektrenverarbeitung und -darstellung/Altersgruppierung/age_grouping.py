import numpy as np
import pandas as pd

from  Variables.constants import *

def check_bound(bound_diff, bound_key):
    match bound_key:
        case 'lower':
            for pos in bound_diff:
                if pos<0: #wenn eine negative Stelle vor einer positiven kommt ist der Patient jünger
                    return False
                elif pos>0: #wenn eine positive Stelle vor einer negativen kommt ist der Patient älter
                    return True
            return False # ansonsten sind alle Stellen 0 und der Patient ist gleich alt
                             # da der Patient allerdings gleich alt sein sollte, darf das nicht sein
        case 'upper':
            for pos in bound_diff:
                if pos>0:
                    return False # Patient ist älter als die obere Grenze
                elif pos<0:
                    return True # Patient ist jünger als die obere Grenze
            return True # Patient ist gleich alt wie die obere Grenze (was erlaubt ist)
        
def alters_gruppe(alter,gruppe):
    upper_bound = UPPER_BOUNDS[gruppe]
    lower_bound = LOWER_BOUNDS[gruppe]
    upper_diff = alter - upper_bound
    lower_diff = alter - lower_bound
            
    return (check_bound(lower_diff,'lower') & check_bound(upper_diff,'upper'))

# Konvertiere Alter in ein standardisiertes Jahr, um teilen zu können
# alter ist ein array
def convert_age(alter):
    return np.sum(np.multiply(alter,MULTIPLIKATOR_ALTER))

def erstelle_alterkateg_df(df_befund):
    alter_serie = df_befund['Alter']

    alter_groups_indices = {}
    for alter_selec in ALTERSGRUPPE_NAMEN:
        group = alter_serie.apply(lambda x: alters_gruppe(x.to_numpy(),alter_selec),axis=1)
        group = group[group].index

        alter_groups_indices[alter_selec] = group
        
    del group, alter_selec

    # erstelle einen Dataframe, der die Altersgruppe festhält
    for alter_selec in ALTERSGRUPPE_NAMEN:
        df_befund.loc[alter_groups_indices[alter_selec],("Alterskategorie","")] = alter_selec

    return None

def alter_ausformuliert(alter_selec):
    prefix = 'bis einschließlich '
    match alter_selec:
        case 'bis3M':
            return prefix+'3 Monate'
        case 'bis2J':
            return prefix+'2 Jahre'
        case 'bis12J':
            return prefix+'12 Jahre'
        case 'bis60J':
            return prefix+'60 Jahre'
        case 'ue60J':
            return 'über 60 Jahre'