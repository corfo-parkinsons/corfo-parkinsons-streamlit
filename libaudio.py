import glob
import pandas as pd
from pydub import AudioSegment

files = sorted(glob.glob('AUDIO/*.wav'))

lens=[AudioSegment.from_file(file).duration_seconds
        for file in files]  

jdf = pd.read_csv('medicionesSergio.csv')
df = pd.DataFrame(dict(file=files, length=lens))
jdf['duration'] = [round(jl,2) for jl in df['length']]  
