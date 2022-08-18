from newaudio import *
sd=SoundData('*Daniela*mp3')
st.df2
sd.df2
for fn, row in sd.df.iterrows():
    print(fn)
    print(row.to_dict())
for fn, row in sd.df.iterrows():
    print(fn)
    open(fn.replace('.mp3','.txt'),'w').write(str(row.to_dict()))
ls
!git add *Danie*txt
%hist -f text_reports.py
