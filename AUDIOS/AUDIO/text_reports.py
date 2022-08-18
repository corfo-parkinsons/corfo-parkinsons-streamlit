from newaudio import *

sd=SoundData('*Daniela*mp3')
for fn, row in sd.df.iterrows():
    print(fn)
    open(fn.replace('.mp3','.txt'),'w').write(str(row.to_dict()))
