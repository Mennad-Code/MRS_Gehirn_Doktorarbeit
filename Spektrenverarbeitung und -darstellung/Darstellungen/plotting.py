import matplotlib.pyplot as plt
import numpy as np
from Postprocessing.data_sanitizing import isolate_signifcant_digit, spec_selec_dataset
from Variables.constants import LOWER_BOUNDS, UPPER_BOUNDS, STD_COLOR
from matplotlib.colors import Normalize
from matplotlib import cm
import seaborn as sns

def plot_spectra(df_chemshift,df_spec,index):
    chemshift = df_chemshift.loc[index,:]
    spektren = df_spec.loc[index,:]
    plt.plot(chemshift.T, spektren.T,linewidth= 1)
    plt.gca().xaxis.set_inverted(True)
    return None

def create_colorbar(alter_selec, palette, ax,interval_n):
    if alter_selec=="bis3M":
        einheiten = "Monaten"
        cbar_lbound = isolate_signifcant_digit(LOWER_BOUNDS[alter_selec])
        cbar_ubound = isolate_signifcant_digit(UPPER_BOUNDS[alter_selec])
    elif alter_selec=="bis2J":
        einheiten = "Monaten"
        cbar_lbound = 3
        cbar_ubound = 24
    else:
        cbar_lbound = isolate_signifcant_digit(LOWER_BOUNDS[alter_selec])
        cbar_ubound = isolate_signifcant_digit(UPPER_BOUNDS[alter_selec])
        einheiten = "Jahren"
    norm = Normalize(vmin=cbar_lbound, vmax=cbar_ubound)
    sm = cm.ScalarMappable(cmap=palette,norm = norm)
    cbar = plt.colorbar(sm,ax=ax, fraction=0.05, pad=0)
    cbar.set_label('Alter in '+einheiten, fontsize=6,labelpad=1)

    # setze die Tick-Intervalle und -Größe
    cbar.set_ticks(np.linspace(norm.vmin, norm.vmax, interval_n))
    cbar.set_ticklabels(np.round(np.linspace(norm.vmin, norm.vmax, interval_n),1))
    cbar.ax.tick_params(size=3, labelsize=3, width= 0.1, pad=0.05)
    
    return None

def plot_distribution(data,title,ax): #Altersverteilung
    bins = np.arange(start=0,stop=90,step=2)
    counts, _ = np.histogram(data,bins)
    sns.histplot(data, bins=bins, kde=False, ax=ax)
    ax.set_ylim(top=np.max(counts)*1.2)
    
    mean = np.mean(data)
    std = np.std(data)
    ax.errorbar(mean, np.max(counts)*1.1 , xerr=std, fmt='o', color='black', capsize=3, capthick=1)

    n = len(data)
    ax.text(0.95, 0.8, f'n = {n}', transform=ax.transAxes, 
            fontsize=6, verticalalignment='top',horizontalalignment='center')
    ax.text(.95, 0.7, f'Ø = {mean:.1f}', transform=ax.transAxes, 
            fontsize=6, verticalalignment='top',horizontalalignment='center')

# Alterhistogramm für alle Datensätze
def alter_histogramm(ds,alter_categ=None,vp=None,diag=None, diag_categ=None, i=1, ax=None,excluded=False):
    df_befund,_,_,_,_ = ds.dataset.load_dataset(i)
    index_selec = spec_selec_dataset(ds, alter_categ, vp, diag, diag_categ, i, excluded=excluded)
    n = len(index_selec) #Gesamtzahl der betrachteten Spektren

    alter_auswahl = df_befund['Alter']['Jahre'].loc[index_selec]

    if not ax:
        fig = plt.figure(figsize=(10, 10))
        fig.suptitle(vp)
        ax = fig.add_subplot(1,1,1)
    else:
        fig = ax.get_figure()

    bins = np.arange(start=0,stop=90,step=2)
    counts, _ = np.histogram(alter_auswahl,bins)
    sns.histplot(alter_auswahl, color=STD_COLOR, bins=bins, kde=False, ax=ax)

    # Fehlerbalken
    mean = np.mean(alter_auswahl)
    std = np.std(alter_auswahl)
    ax.errorbar(mean, np.max(counts)*1.1 , xerr=std, fmt='o', color='black', capsize=3, capthick=1)

    # Kofiguration der Achsen
    ax.set_ylim(top=np.max(counts)*1.2) # dadurch hat der Fehlerbalken auch noch Platz
    ax.set_ylabel('Anzahl der Spektren')
    ax.set_xticks(np.arange(start=0,stop=90,step=2))

    for label in ax.get_xticklabels()[::2]: #zu dichte Achsenbeschriftung anpassen
        label.set_visible(False)

    ax.text(0.95, 0.8, f'n = {n}', transform=ax.transAxes, 
                fontsize=8, verticalalignment='top',horizontalalignment='center') # Gesamtzahl der Spektren
    
    ax.text(.95, 0.7, f'Ø = {mean:.1f}', transform=ax.transAxes, 
            fontsize=8, verticalalignment='top',horizontalalignment='center') # Spektrendurchschnitt
    
    return fig