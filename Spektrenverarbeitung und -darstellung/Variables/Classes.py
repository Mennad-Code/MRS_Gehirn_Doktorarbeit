import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from Variables.constants import DIAG_KATEG_NAMEN, CATEG_PALETTE

from Darstellungen.axis_config import *
from Postprocessing.data_sanitizing import spec_selec
from Postprocessing.averaging import *

from ipywidgets import interact, IntSlider, Checkbox, Output, widgets, SelectMultiple, Layout, HBox, VBox

#Klasse, die alle Datensätze enthält
class dataset:
    def __init__(self,df_befund_dict, spec_dict, chemshift_dict, ref_spec_df_dict,ref_chemshift_df_dict):
        self.df_befund_dict = df_befund_dict
        self.spec_dict = spec_dict
        self.chemshift_dict = chemshift_dict
        self.ref_spec_df_dict = ref_spec_df_dict
        self.ref_chemshift_df_dict =  ref_chemshift_df_dict
    def load_dataset(self,i):
            return self.df_befund_dict[i], self.spec_dict[i], self.chemshift_dict[i], self.ref_spec_df_dict[i],self.ref_chemshift_df_dict[i]
    
class dataset_categ(dataset):
    def __init__(self,dataset,kategorienliste):
        self.dataset = dataset
        self.kategorienliste = kategorienliste

        for i, (j,df) in enumerate(self.dataset.df_befund_dict.items()):
            categ_list = []
            for diag in df['Befund']: #diag ist Diagnose des ausgewählten Spektrums
                if ',' in diag: # bei mehreren Diagnosen: nehme die erste
                    diag = diag.split(',')[0]
                col = np.any(kategorienliste.isin([diag]), axis=0)
                if np.any(col,axis=None):
                    col = col[col].index[0]
                else:
                    # Markiere nicht zugeordnete Diagnosen als "Nicht bekannt"
                    col = 'Nicht bekannt'
                categ_list.append(col)
            df.insert(2,"Diagnosekategorie",value=categ_list)

    # plotte mit bekannter Kategorienliste
    def plot_categ_specs(self,i):
        df_befund,df_spec,df_chemshift,_,_ = self.dataset.load_dataset(i)

        new_x = new_x_values(df_chemshift)
        df_spec_interpol = interpoliere_spektren(df_spec,df_chemshift,new_x)

        for i,categ in enumerate(self.kategorienliste.columns):
                index_temp = spec_selec(df_befund,df_spec,diag_categ=categ)

                avg_spec = df_spec_interpol.loc[index_temp].mean(axis=0)
                std_spec = df_spec_interpol.loc[index_temp].std(axis=0)
                sns.lineplot(avg_spec,linewidth=.5)
                plt.fill_between(new_x,avg_spec-std_spec*.2,avg_spec+std_spec*.2,alpha=0.25,linewidth=.25)

                basic_axis_config(plt.gca())

    #plotte nach neuer Kategorienliste
    def plot_categ_specs_new_categ(self,i,kategorienliste,ax=None):
        df_befund,df_spec,df_chemshift,_,_ = self.dataset.load_dataset(i) #lade relevante Liste

        # hier wird einfach nur die Kategorien in die Serie categ_temp eingetragen
        if isinstance(kategorienliste,pd.core.frame.DataFrame):
            print('hello')
            categ_temp = df_befund['Befund'].map(lambda x: kategorienliste.columns[kategorienliste.isin([x]).any(axis=0)].values[0]
                            if kategorienliste.columns[kategorienliste.isin([x]).any(axis=0)].values else
                            'Nicht bekannt') #erstelle neue Kategorienserie
        elif isinstance(kategorienliste,list):
            categs = self.kategorienliste.columns
            diag_list = [row.children[1].value for row in kategorienliste]
            categ_temp = df_befund['Befund'].map(lambda x: categs[[x in diag for diag in diag_list]].values[0]
                        if categs[[x in diag for diag in diag_list]].values else
                        'Nicht bekannt') #erstelle neue Kategorienserie

        new_x = new_x_values(df_chemshift) #erstelle zu verwendende Chemical-Shift-Werte
        df_spec_interpol = interpoliere_spektren(df_spec,df_chemshift,new_x) #erstelle die interpolierten Spektren

        legal_indices = spec_selec(df_befund,df_spec) # erlaubte Indices, die benutzt worden sind

        for i,categ in enumerate(self.kategorienliste.columns):
            index_temp = categ_temp.loc[legal_indices].loc[categ_temp.loc[legal_indices]==categ].index #bisschen hässlicher Syntax, könnte ich noch ändern

            avg_spec = df_spec_interpol.loc[index_temp].mean(axis=0)
            std_spec = df_spec_interpol.loc[index_temp].std(axis=0)

            if ax:
                sns.lineplot(avg_spec,linewidth=.5,ax=ax)
                ax.fill_between(new_x,avg_spec-std_spec*.2,avg_spec+std_spec*.2,alpha=0.25,linewidth=.25)
            else:
                sns.lineplot(avg_spec,linewidth=.5)
                plt.fill_between(new_x,avg_spec-std_spec*.2,avg_spec+std_spec*.2,alpha=0.25,linewidth=.25)

        if ax:
            return basic_axis_config(ax)
        else:
            basic_axis_config(plt.gca())