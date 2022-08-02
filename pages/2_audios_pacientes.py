import altair as alt
import pandas as pd
import glob

from s3link import *
from aws import s3_audio_list, audio_data
from plotters import plot_wave, plot_spec, dubread

import streamlit as st

url1 = 'https://share.streamlit.io/sergiolucero/st1/main/app.py'
url2 = url1.replace('st1','st2')

st.set_page_config(
    page_title="Audios Parkinson", page_icon="*", layout="wide"
)

st.title("Audios Parkinson")
st.write("registro de medicaciones y mediciones de pacientes")

html = f'<A HREF="{url1}">Farmacodinámica</A>'
#st.components.v1.html(html)

#title = f'Frecuencias normalizadas {paciente}'
#charts = []
audio_datos = s3_audio_list()

# leer y cruzar datos DynamoDB
dd_df = audio_data(True)
#dd_df['time'] = dd_df['time'].apply(str)
st.header('audio_data (from DynamoDB)')
st.write(dd_df)

#st.write('NADa=', len(audio_datos))
st.header('audio_datos (from s3)')
#st.write(audio_datos)
ad1 = dd_df[dd_df.id.str.contains('AUDIO')]   # the NEW
ad2 = dd_df[dd_df.data.str.contains('JOMAX')]

for _, row in ad2.iterrows():
# una fila por cada registro existente
    row_dict = row['data']
    #filename = 'AUDIO/NEW/'+fn.replace('.ogg','.wav')
    #if fecha in ('2022-07-29','2022-07-30',):
    st_write(row_dict)
    #st.write(f'Fecha: {fecha} Hora: {hora}  [Archivo: {filename}')

    # [1] fecha/hora
    # [2] print coefs
        # try to match!
    if False:
        audio_bytes = open(filename, 'rb').read()
        y,sr = dubread(filename)

        col1, col2 = st.columns([1,1])
        with col1:
            st.pyplot(plot_wave(y, sr))
        with col2:   # audio was inside col3
            st.audio(audio_bytes, format='audio/wav')
            st.pyplot(plot_spec(y, sr))
