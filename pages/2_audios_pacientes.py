import altair as alt
import pandas as pd
import glob
from s3link import *

from plotters import plot_wave, plot_spec, dubread

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

url1 = 'https://share.streamlit.io/sergiolucero/st1/main/app.py'
url2 = url1.replace('st1','st2')

st.set_page_config(
    page_title="Audios Parkinson", page_icon="*", layout="wide"
)

st.title("Audios Parkinson")
st.write("registro de medicaciones y mediciones de pacientes")

html = f'<A HREF="{url1}">Farmacodinámica</A>'
#st.components.v1.html(html)

def aggrid_interactive_table(df: pd.DataFrame):
    
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True)

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="dark", height=200,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection

sdf = pd.read_csv('medicionesSergio.csv')
adict = {f'F{ix}':['min','mean','max'] for ix in range(5)}
gdf = sdf.groupby('Paciente', as_index=False).agg(adict).round(1)
#st.write(gdf)
gdf = pd.DataFrame(gdf)
gdf.columns = [''.join(gc) for gc in gdf.columns]
#st.write(gdf.columns)

selection = aggrid_interactive_table(df=gdf)

if selection:
    try:
        paciente = selection["selected_rows"][0]['Paciente'] 
    except:
        paciente = 'Paciente 2'
    #pdf = sdf[sdf.Paciente==paciente]
    #pdf['fecha'] = pdf['Archivo audio'].apply(lambda aa: aa.split('_')[1])
    
    #st.write("You selected:", paciente) #, pdf.columns)
    #st.json(selection["selected_rows"])
    title = f'Frecuencias normalizadas {paciente}'
    charts = []
    #for f in range(5):
    #    ndf = pdf.copy(); nc=f'F{f}'
    #    ndf[nc]/=ndf[nc].max()
    #    charts.append(alt.Chart(ndf, title=title).mark_line().encode(x=alt.X("fecha", axis=alt.Axis(labelAngle=0)),        ## wanna rotate!
    #                                                                 y=alt.Y(f"F{f}", scale=alt.Scale(zero=False))))

    if False:  # NOT TONIGHT dear
        pass
        #st.altair_chart((charts[0]+charts[1]+charts[2]+charts[3]+charts[4]).configure_title(fontSize=24).interactive(), 
        #            use_container_width=True)
    
    ## ahora los audios
    ## plots stolen from: https://github.com/phrasenmaeher/audio-transformation-visualization/blob/main/visualize_transformation.py

    audio_data = user_oggs('JOMAX')
    #st.write('4reals?')
    audio_data = pd.read_csv('cheater.csv')
    st.write(audio_data)

    #audios = glob.glob('AUDIO/NEW/*.wav')
    #audios = [fn.replace('AUDIO/NEW/','') for fn in audios if 'JOMAX' in fn]
    #st.write(audios)

    

    for _, row in audio_data.iterrows():   # una fila por cada registro existente
        fecha, hora, size, fn = row.values

        filename = 'AUDIO/NEW/'+fn.replace('.ogg','.wav')
        st.write(fn)
        # [1] fecha/hora
        # [2] print coefs




    #for _, row in pdf.iterrows():   # una fila por cada registro existente
        #st.write(row['fecha'])
        #filename = 'PACIENTES/'+row['Archivo audio']
        audio_bytes = open(filename, 'rb').read()
        y,sr = dubread(filename)
        
        col1, col2 = st.columns([1,1])
        with col1:
            st.pyplot(plot_wave(y, sr))
        with col2:   # audio was inside col3
            st.audio(audio_bytes, format='audio/wav')
            st.pyplot(plot_spec(y, sr))
