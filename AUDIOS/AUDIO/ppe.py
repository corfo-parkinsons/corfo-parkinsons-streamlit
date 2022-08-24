from math import log
import numpy as np
import spectrum
from scipy.signal import lfilter

def arcov(x, p):
    [A, E] = spectrum.covar.arcovar(x,p)
    A = np.hstack((1,A)) # MATLAB gives back initial value 1, so we do the same 
    return A
def entropy(f):
    return -sum(fj * log(fj) for fj in f if fj>0);
################

def PPE(sound):
    F0meanHC=120
    F0 = sound.to_pitch().selected_array['frequency']
    F0 = [fx for fx in F0 if fx>0]
    logF0=[log(F0x/F0meanHC) for F0x in F0]   # corta hasta F0==0
    ARcoef=arcov(logF0, 10)
    sig = lfilter(ARcoef, 1, logF0)
    minS = np.min(sig); maxS = np.max(sig); dS = (maxS-minS)/100
    PPEd = np.histogram(sig, bins=100)[0]

    return entropy(PPEd/sum(PPEd))/log(len(PPEd))
