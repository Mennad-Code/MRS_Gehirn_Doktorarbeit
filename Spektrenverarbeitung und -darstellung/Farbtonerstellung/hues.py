from Variables.constants import *
from Altersgruppierung.age_grouping import convert_age
from itertools import compress

def determine_single_hue(alter,alter_categ):
    intervall_pos = alter-LOWER_BOUNDS[alter_categ]
    hue = convert_age(intervall_pos)/convert_age(INTERVALLGROESSE_ALTERSGRUPPEN[alter_categ])
    return hue

def determine_hues(df_befund):
    df_befund.loc[:,("Farbton","")] = df_befund.apply(lambda x: determine_single_hue(x["Alter"].values,x["Alterskategorie"].values[0]), axis=1)
    return None

def select_palette(vp_select):
    if vp_select:
        return PALETTES[vp_select]
    else:
        return sns.color_palette("blend:#051590,#f171f8", as_cmap = True)
    
# Für die Kategorien: Wähle bei Kategorienzählung die passende Farbe für die Darstellung aus

def color_selec_categ_histogram(count,kategorienliste):
    reihenfolge_diagkateg = kategorienliste.columns
    return count.index.map(lambda x: list(compress(CATEG_PALETTE,reihenfolge_diagkateg == x))[0])