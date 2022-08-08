import streamlit as st
from aws import *
import aws

adf = scan_table('audios_pacientes')
adf = adf[adf.id.str.contains('.mp3')]
st.header('Audios Fase Agosto')
ROOT = 'https://quantcldata.s3.us-east-2.amazonaws.com/AUDIOS'
rt = lambda dato: "<A HREF='%s/%s'>archivo</A>" %(ROOT, dato) 

for col in ['user','date','coefs']:
    adf[col] = adf.data.apply(lambda d: eval(d).get(col))
adf = adf.sort_values('date', ascending=False)
adf['link']= [rt(dato) for dato in adf.data]
adf = adf.drop('data', axis=1)
st.dataframe(adf)

## ahora los links de descarga
ht = lambda x: st.markdown(x, unsafe_allow_html=True)
html_string = '<TABLE BORDER=1><TR><TH>user</TH><TH>date</TH><TH>Coeficientes</TH><TH>Descarga</TH></TR>'
for _, row in adf.iterrows():
    html_string += '<TR>
    for var in ['user','date','coefs','link']:
        html_string += '<TD>%s</TD>' %row[var]
    html_string+='</TR>'
ht(html_string+'</TABLE>')
