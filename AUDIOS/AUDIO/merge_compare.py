import glob
txt={fn: eval(open(fn):read()) for fn in glob.glob('AUDIOS/AUDIO/*.txt')}
txt={fn: eval(open(fn).read()) for fn in glob.glob('AUDIOS/AUDIO/*.txt')}
len(txt)
import pickle
pickle.dump(txt, open('AUDIOS/AUDIO/36txt.pk','wb'))
cd AUDIOS/AUDIO
!mkdir comp1
!mv 36txt.pk comp1/
!aws s3 cp s3://quantcldata/AUDIOS/PraatAudios1.xlsx comp1/
ls comp1
%hist
import pandas as pd
ddf=pd.read_excel('comp1/PraatAudios1.xlsx', sheet_name=None)
ddf.keys()
ddf['Hoja1']
out_dani={}
for df in ddf.values():
    print(df.columns[0])
for df in ddf.values():
    print(df.columns[0])
    fn=df.columns[0].split()[-2]
    out_dani[fn]=df.iloc[6:]
    print(fn, out_dani[fn].head())
%hist
txt
%hist
# now compare every out_dani to txt
txt.keys()
out_dani.keys()
for dk, dani_df in out_dani.items()import osmnx as ox
place = "Concon, Chile"
restaurant_amenities = ['restaurant', 'museum']
for dk, dani_df in out_dani.items():
    text_df = txt['AUDIOS/AUDIO/'+dk+'.txt']
for dk, dani_df in out_dani.items():
    text_df = txt['AUDIOS/AUDIO/'+dk+'.txt']
text_df
out_dani
dani_df.head()
text_df
dani_df.head()
dani_df.iloc[2:10]
[(k,txt_df[k]) for k in txt_df.keys() if 'pitch' in k]
[(k,text_df[k]) for k in txt_df.keys() if 'pitch' in k]
[(k,text_df[k]) for k in text_df.keys() if 'pitch' in k]
dani_df.iloc[2:10]
%hist -f merge_compare.py
