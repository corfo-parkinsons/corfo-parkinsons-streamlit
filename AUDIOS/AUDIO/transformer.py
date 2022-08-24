import glob
from audio import ogg2wav
import os
from config import IN_FMT, OUT_FMT

for fn in glob.glob('*'+IN_FMT):
    ofn = fn.replace(IN_FMT, OUT_FMT)
    if not os.path.exists(ofn):
        print(fn)
        ogg2wav(fn)
