import streamlit as st
from aws import *
import aws

adf = scan_table('audios_pacientes')
adf = adf[adf.id.str.contains('.mp3')]
st.header('Audios Fase Agosto')

for col in ['user','date','coefs']:
    adf[col] = adf.data.apply(lambda d: eval(d).get(col))

adf = adf.drop('data', axis=1)
adf = adf.sort_values('date')
st.dataframe(adf)

## ahora los links de descarga
#AUDIO/5221716593_JOMAX_Contacto_1357.mp3
ROOT = 'https://quantcldata.s3.us-east-2.amazonaws.com/AUDIOS/'
for _, row in adf.iterrows():
    url = ROOT+row['id']
    html_string = f"<A HREF='{url}'>Descargar {row['id']}</A>"
    st.markdown(html_string, unsafe_allow_html=True)
