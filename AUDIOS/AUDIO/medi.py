import pickle
dm=pickle.load(open('dani_mine.pk','rb'))
dm.keys()[0]
dm.keys()
#k0=list(dm.keys())[0]
d0,m0=dm[k0]
d0
m0
for mk, mv in m0.items():
    print(mk,mv)
    dv = d0[d0[d0.columns[0]].str.contains(mk)]
    print(dv)
for mk, mv in m0.items():
    if mk[:4] not in ('Dura'):
        print(mk,mv)
        dv = d0[d0[d0.columns[0]].str.contains(mk)]
        print(dv)
d0.dropna()
d0.iloc[2:34]
d0.iloc[2:33]
d0.tail(10)
d0.iloc.tail()
d0.tail()
d0=d0.iloc[2:33].append(d0.tail)
d0=d0.iloc[2:33].append(d0.tail())
d0
for mk, mv in m0.items():
    if mk[:4] not in ('Dura'):
        print(mk,mv)
        dv = d0[d0[d0.columns[0]].str.contains(mk)]
        print(dv)
for mk, mv in m0.items():
    if mk[:4] not in ('Dura'):
        print('MINE:',mk,mv)
        dv = d0[d0[d0.columns[0]].str.contains(mk)]
        print('DANI:',dv.values)
d0
m0
pd
import pandas as pd
pd.DataFrame(m0)
pd.DataFrame(m0,index=[0])
pd.DataFrame(m0,index=[0]).T
dm0=pd.DataFrame(m0,index=[0]).T
d0
%hist -f medi.py
