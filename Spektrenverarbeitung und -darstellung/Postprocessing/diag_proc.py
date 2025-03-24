from Postprocessing.data_sanitizing import spec_selec, entferne_irr_vp

def häufigste_befunde_diag(df_befund,df_spec,minimum_n=10):
    index_usable = spec_selec(df_befund,df_spec)
    
    # es sollen nur die zwei wichtigsten Voxelpositionen gewählt werden
    index_usable = entferne_irr_vp(df_befund,index_usable)

    einzeldiag_count = df_befund['Befund'].loc[index_usable].value_counts()
    einzeldiag_selec = einzeldiag_count.loc[einzeldiag_count>=minimum_n]

    einzeldiag_selec = einzeldiag_selec.index

    einzeldiag_selec_indices = {}

    for einzeldiag in einzeldiag_selec:
        index_temp = df_befund["Befund"].loc[index_usable]==einzeldiag
        einzeldiag_selec_indices[einzeldiag] = index_temp[index_temp].index

    return einzeldiag_selec_indices