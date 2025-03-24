import numpy as np

def ceil_to_first_sign_dig(num):
    num = np.abs(num) # positiv
    scaled = num / (10 ** np.floor(np.log10(num))) #skaliere zwischen 1 und 10
    scaled = np.ceil(scaled)
    num_proc = np.ceil(scaled)*(10**np.floor(np.log10(num))) #reskaliere
    return num_proc