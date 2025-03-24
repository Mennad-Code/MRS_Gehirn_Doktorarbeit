import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from Farbtonerstellung.hues import color_selec_categ_histogram

def axis_config_einzeldiag(j,i,ax,vp_selec,index_temp):
    # Füge die Voxelpositions-Beschreibung hinzu
    ax.text(.05,.9,vp_selec, transform=ax.transAxes,fontsize=6)
    ax.set_xlim(left=-.5,right=4.5)
    ax.xaxis.set_inverted(True)

    if j==0:
        ax.set_title(chr(65+i),loc='left')
        ax.grid(True)
        ax.set_xticklabels('')
        ax.set_xlabel('')
    elif j==1:
        ax.set_xlabel('Frequenz (ppm)',fontsize=6,labelpad=8)
        ax.tick_params(axis='x',labelsize=5,pad=-4)
        
    if not index_temp.empty:
        ax.set_yticks([])
        ax.set_ylabel('Amplitude',fontsize=6,labelpad=8)

        # Füge die Anzahl der Spektren n hinzu
        ax.text(0.8,0.9,'n = '+ str(len(index_temp)), fontsize=6, transform=ax.transAxes)

    # falls leer: fülle den Plot mit dem dementsprechenden Hinweis aus
    else:
        t = ax.text(0.5,0.5, 'keine Spektren in dieser Gruppe',transform=ax.transAxes,fontsize=6)
        t.set_ha('center')
        ax.set_yticks([])

    return ax

def axis_config_histo(j,i,vp_selec,ax,index_temp):
    ax.text(.95, .9, f'{vp_selec}', transform=ax.transAxes, 
            fontsize=6, verticalalignment='top',horizontalalignment='center')
    ax.set_xlim(left=-20,right=90)
    
    if j==0:
        ax.set_title(chr(65+i),loc='left')

    if not index_temp.empty:
        ax.set_ylabel('Anzahl der Spektren',fontsize=6)

        if j==0:
            ax.set_title(chr(65+i),loc='left')
            ax.grid(True)
            ax.set_xticklabels('')
            ax.set_xlabel('')
            ax.set_ylabel('Anzahl der Spektren',fontsize=6)
            ax.tick_params(axis='y',labelsize=6,pad=0)
        elif j==1:
            ax.set_ylabel('Anzahl der Spektren',fontsize=6)
            ax.set_xlabel('Alter des Patienten (in Jahren)',fontsize=6)
            ax.tick_params(axis='y',labelsize=6,pad=0)
            ax.tick_params(axis='x',labelsize=5,pad=0)
    else:
        if j==0:
            ax.set_title(chr(65+i),loc='left')
            ax.grid(True)
            ax.set_xticklabels('')
            ax.set_xlabel('')
            
        t = ax.text(0.5,0.5, 'keine Spektren in dieser Gruppe',transform=ax.transAxes,fontsize=6)
        t.set_ha('center')
        ax.set_yticks([])

    return ax

# Setze xmax und xmin und drehe die x-Achse
def basic_axis_config(ax,min=0.11,max=4.30):
    ax.set_xlim(left=min,right=max)
    ax.xaxis.set_inverted(True)
    ax.set_yticks([])
    return ax

# Axenkonfiguration für die Referenzspektren
def axis_config_refs(n,j,ax,vp_selec):
    # Füge die Voxelpositions-Beschreibung hinzu
    ax.text(.05,.9,vp_selec, transform=ax.transAxes,fontsize=6)
    ax.set_xlim(left=-.5,right=4.5)
    ax.xaxis.set_inverted(True)

    if j==0:
        ax.set_title(chr(64+n),loc='left')
        ax.grid(True)
        ax.set_xticklabels('')
        ax.set_xlabel('')
    elif j==1:
        ax.set_xlabel('Frequenz (ppm)',fontsize=6,labelpad=8)
        ax.tick_params(axis='x',labelsize=5,pad=-4)

    ax.set_yticks([])
    ax.set_ylabel('Amplitude',fontsize=6,labelpad=8)

    ax.legend().remove()
        
    return ax

# Axenkonfiguration für die Kategoriendurchschnittsdarstellung
def axis_config_categ(ax,index_selec,abb_n):
    # konfiguriere x-Achse
    ax.set_xlim(left=-.5,right=4.5)
    ax.xaxis.set_inverted(True)

    
    ax.set_title(chr(65+abb_n),loc='left')
    ax.grid(True)
    
    ax.set_xlabel('Frequenz (ppm)',fontsize=15,labelpad=8)
    ax.tick_params(axis='x',labelsize=15,pad=-4)
    
    ax.set_yticks([])
    ax.set_ylabel('Amplitude',fontsize=15,labelpad=8)

    # Füge die Anzahl der Spektren n hinzu
    ax.text(0.8,0.9,'n = '+ str(len(index_selec)), fontsize=15, transform=ax.transAxes)

    return ax

# Axenkonfiguration für die Kategorienhistogrammdarstellung

def categ_histogram(count,kategorienliste,ax=None):
     if not ax:
          _, ax = plt.subplots()
     if len(count)>=5:
          ax = count[range(5)].plot(kind='bar',color=color_selec_categ_histogram(count,kategorienliste),ax=ax)
     else:
          ax = count.plot(kind='bar',color=color_selec_categ_histogram(count,kategorienliste),ax=ax)
     ax.set_xticks([])
     ax.set_ylabel('Anzahl der Spektren',size=12)
     ax.yaxis.set_label_position("right")
     ax.set_xlabel('')
     if count.max()>1:
          ax.set_yticks(range(0, count.max() + 1, 2))
          for label in ax.get_yticklabels()[::2]:
               label.set_visible(False)
     else:
          ax.set_yticks([1])
     ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
     ax.tick_params(axis='y',labelsize=15)

     return ax