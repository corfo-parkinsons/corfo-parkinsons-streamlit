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
st.write("[registro de mediciones de pacientes]")

html = f'<A HREF="{url1}">Farmacodinámica</A>'
#st.components.v1.html(html)

#title = f'Frecuencias normalizadas {paciente}'
#charts = []
audio_datos = s3_audio_list()

# leer y cruzar datos DynamoDB
dd_df = audio_data(True)
dd_df = dd_df[dd_df.data.str.contains('JOMAX')]
#dd_df['time'] = dd_df['time'].apply(str)
#st.header('audio_data (from DynamoDB)')
##st.write(dd_df)

#st.write('NADa=', len(audio_datos))
#st.header('audio_datos (from s3)')
audio_datos = audio_datos[audio_datos.filename.str.contains('JOMAX')]
s3ogg_datos = audio_datos[audio_datos.filename.str.contains('.ogg')]  # original
s3mp3_datos = audio_datos[audio_datos.filename.str.contains('.mp3')]  # modified

#st.write(audio_datos)  # reading filenames from s3 (mp3/ogg -> mod_date!)
from config import IN_FMT, OUT_FMT
#st.write('-'*80)
for _, ogg_row in s3ogg_datos.iterrows():
    ogg_filename, timedata = ogg_row.values
    # look up mp3 (info)
    matcher = ogg_filename.replace(IN_FMT, '')
    #st.write(ogg_filename, matcher)
    match = s3mp3_datos[s3mp3_datos.filename.str.contains(matcher)]  # mp3_file
    mp3_file = match.iloc[0]['filename']
    #st.write(match, mp3_file)
    st.write(mp3_file.replace('AUDIOS/AUDIO/',''))
    audio_bytes = open(mp3_file, 'rb').read()
    wav_file = mp3_file.replace('.mp3','.wav')
    y,sr = dubread(wav_file)   # fix this!

    col1, col2 = st.columns([1,1])
    with col1:
        #pass
        st.pyplot(plot_wave(y, sr))
    with col2:   # audio was inside col3
        st.audio(audio_bytes, format='audio/wav')   
        #st.audio(audio_bytes, format='audio/mp3')   
        st.pyplot(plot_spec(y, sr))
