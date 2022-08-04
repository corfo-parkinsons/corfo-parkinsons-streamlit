import streamlit as st
from aws import *
import aws

adf = scan_table('audios_pacientes')
adf = adf[adf.id.str.contains('.mp3')]
st.header('Audios Fase Agosto')



st.dataframe(adf)
