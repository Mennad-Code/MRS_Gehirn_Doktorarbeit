import glob
import os
import scipy as sci
import pandas as pd
from Variables.constants import *

def get_fname(s):
    return glob.glob(os.path.join(os.getcwd(),s))[0]

# erstellt ein Dataframe aus den .mat-Dateien
def load_mat_file(filename):
    temp = sci.io.loadmat(get_fname(filename))
    temp = temp['spektren_struct'][0]
    temp = pd.DataFrame.from_records(temp)
    return temp

#flatten alle Inhalte und erstelle ein regelrechtes Dataframe
def extrahiere_df(df):
    indices = pd.Index(df['IDs'][0].squeeze())
    indices = pd.Index(indices)
    df_spec = pd.DataFrame(df['Spektren'][0], index = indices)
    df_chemshift = pd.DataFrame(df['Chemshift'][0], index = indices)
    return df_spec, df_chemshift

def erstelle_spec_chem_df(filepath):
    os.chdir(filepath)
    spec_dict = {}
    chemshift_dict = {}

    for i, name in enumerate(FILE_NAMES):
        temp = load_mat_file(name)
        df_spec, df_chemshift = extrahiere_df(temp)
        spec_dict[i+1], chemshift_dict[i+1] = df_spec, df_chemshift

    return spec_dict, chemshift_dict

def erstelle_df_befund_dict(filepath):
    os.chdir(filepath)
    df_befund_dict = {}

    for i,name in enumerate(FILE_NAMES):
        df_befund_dict[i+1] = pd.read_excel(get_fname(name), index_col=0, header=[0,1])

        col_names = df_befund_dict[i+1].columns.get_level_values(1)

        for col in col_names[range(0,3)]:
            df_befund_dict[i+1].rename(columns={col:""},level=1,inplace=True)
        
    return df_befund_dict