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
#AUDIO/5221716593_JOMAX_Contacto_1357.mp3
st.markdown('<TABLE BORDER=1><TR><TH>Coeficientes</TH><TH>Descarga</TH></TR>')
for _, row in adf.iterrows():
    html_string = '<TR><TD>%s</TD>' %row['coefs']
    html_string += '<TD>%s</TD>' %row['link']
    st.markdown(html_string, unsafe_allow_html=True)
st.markdown('</TABLE>')
