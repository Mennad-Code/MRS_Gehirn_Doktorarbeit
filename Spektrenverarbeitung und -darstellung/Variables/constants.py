import numpy as np
import seaborn as sns

import colorcet as cc

# Namen der Datensätze
FILE_NAMES = ["*135ms_1,5T*","*30ms_1,5T*","*135ms_3T*","*30ms_3T*"]

# Namen für die wichtigsten Voxelpositionen
VP_NAMES = ["Basalganglien", "Marklager", "Unbekannt"]

# Namen für alle Voxelpositionen
VP_POSITIONEN_VOLLSTAENDIG = ['Marklager','Basalganglien','Kleinhirn','Hirnstamm','Sonstige','Unbekannt']

# Benennung der Statistik nach ein- oder ausgeschlossenen Spektren
NEXC = '_nach_Auschluss.jpeg'
EXC = '_ausgeschlossen.jpeg'

# Namen der Altersgruppen
ALTERSGRUPPE_NAMEN = ['bis3M', 'bis2J', 'bis12J', 'bis60J', 'ue60J']
temp_age_arr = [[0,3,0],[2,0,0],[12,0,0],[60,0,0]]

# Namen der Diagnosekategorien
DIAG_KATEG_NAMEN = ['Erkrankungen des Stoffwechsels der Mono-, Oligo- und Polysaccharide, der Glykopeptide und der Aminoglykoside',
                    'Erkrankungen des Stoffwechsels der verzweigtkettigen Aminosäuren',
                    'Erkrankungen des Stoffwechsels der aromatischen Aminosäuren',
                    'Erkrankungen des Stoffwechsels der schwefelhaltigen und einfache Aminosäuren',
                    'Störungen des Zitratzyklus, der Atmungskette, des mitochondrialen Stoffwechsels und allgemein hypoxisch-ischämische Erkrankungen',
                    'Sphingolipid- und Fettsäure-Stoffwechsel, Myelinisierungsstörungen',
                    'Erkrankungen mit Veränderungen von Signalkaskaden, Proteinfaltung und -modifikation; Strukturprotein-Defekte und Proteinaggregation',
                    'komplexe genetische Störungen und epigenetische Funktionsstörungen',
                    'Ätiologisch ungeklärte Erkrankungen',
                    'Entzündliche Erkrankungen (autoimmun  und infektiös)',
                    'Neo- und Dysplasien',
                    'Sonstige Erkrankungen']

# Intervallgröße für die Altersgruppen
alter_group_interval_temp = [[0,3,0],[1,9,0],[10,0,0],[48,0,0],[25,0,0]]
INTERVALLGROESSE_ALTERSGRUPPEN = {}
for i, group in enumerate(alter_group_interval_temp):
    INTERVALLGROESSE_ALTERSGRUPPEN[ALTERSGRUPPE_NAMEN[i]]  = group
del alter_group_interval_temp, group

# für die Farbtonbestimmung: untere Grenze der einzelnen Altersgruppen
LOWER_BOUNDS = {}

for i, name in enumerate(ALTERSGRUPPE_NAMEN):
    if i == 0:
        LOWER_BOUNDS[name] = np.array([0,0,0])
    else:
        LOWER_BOUNDS[name] = np.array(temp_age_arr[i-1])

# für die Legendenerstellung: auch die obere Grenze
UPPER_BOUNDS = {}
for i, name in enumerate(ALTERSGRUPPE_NAMEN):
    if i == 4:
        UPPER_BOUNDS[name] = np.array([85,0,0])
    else:
        UPPER_BOUNDS[name] = np.array(temp_age_arr[i])

del temp_age_arr

# Multiplikator für das standardisierte Jahr
MULTIPLIKATOR_ALTER = [1, 1/12, 1/(12*30)]

# Dictionary für die Farbpaletten
PALETTES = {}
for i, vp_name in enumerate(VP_NAMES):
    match vp_name:
        # zu verwendende Farbpalette für die VP in den Basalganglien
        case 'Basalganglien':
            PALETTES[vp_name] = palette_bg = sns.color_palette("blend:#051590,#f171f8", as_cmap = True)
        # zu verwendende Farbpalette für die VP im Marklager
        case 'Marklager':
            PALETTES[vp_name] = palette_ml = sns.color_palette("blend:#6CCF0A,#FAA0A3", as_cmap = True)

# Farben für die Kategorien-Darstellung
CATEG_PALETTE = cc.glasbey_category10[:12]

# Standard-Farbe von Seaborn
STD_COLOR = sns.palettes.color_palette("tab10")[0]

#Auswahl der für die Kategoriendarstellung betrachteten Darstellung
ALTER_SELEC_DIAGKATEG = {(1,"Basalganglien"):[0,1,1,1,1], #135ms 1,5T
                         (1,"Marklager"):[0,1,1,1,1],
                         (2,"Basalganglien"):[0,1,1,1,1], #30ms 1,5T
                         (2,"Marklager"):[0,1,1,1,1],
                         (3,"Basalganglien"):[0,1,1,1,1], #135ms 3T
                         (3,"Marklager"):[0,0,0,1,1],
                         (3,"Unbekannt"):[1,1,1,1,1],
                         (4,"Basalganglien"):[0,1,1,1,1], #30ms 3T
                         (4,"Marklager"):[0,0,0,1,1],
                         (4,"Unbekannt"):[1,1,1,1,1]}

# HTML-Zeichen für die IPy-Widget-Darstellung
HTML_SEP = ',<br>'

# Farben für die Referenzspektrendarstellung
REF_COLORS = sns.color_palette("viridis",4)