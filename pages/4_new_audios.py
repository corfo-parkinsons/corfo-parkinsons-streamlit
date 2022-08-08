import streamlit as st
from aws import *
import aws

adf = scan_table('audios_pacientes')
adf = adf[adf.id.str.contains('.mp3')]
st.header('Audios Fase Agosto')

for col in ['user','date','coefs']:
    adf[col] = adf.data.apply(lambda d: eval(d).get(col))

adf = adf.drop('data', axis=1)
#AUDIO/5221716593_JOMAX_Contacto_1357.mp3
ROOT = 'https://quantcldata.s3.us-east-2.amazonaws.com/AUDIOS/'
link = lambda row: "<A HREF='%s'>link</A>"  %(ROOT+row['id'])
adf=adf[adf.id.str.contains('.mp3')]
adf['Descarga'] = adf.apply(link, axis=1)
adf = adf.drop(['id'], axis=1)
#st.dataframe(adf)
adf = adf.sort_values('date', ascending=False)
## hide some!
adf['coefs'] = [{k:v for k,v in c.items() if 'apq' not in k}
                for c in adf.coefs]

st.write(adf.to_html(escape=False, index=False), unsafe_allow_html=True)
#    st.markdown(html_string, unsafe_allow_html=True)
