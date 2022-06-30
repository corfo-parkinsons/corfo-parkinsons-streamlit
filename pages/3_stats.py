import boto3, s3fs
from aws import *

import pandas as pd
import streamlit as st
from collections import Counter

st.set_page_config(
    page_title="Estadísticas Parkinson", page_icon="⬇", layout="wide"
)

fs = s3fs.S3FileSystem(anon=False)
@st.experimental_memo(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")
    
s3 = boto3.resource('s3', region_name='us-east-2')  # should be validated with ENV? credentials
ddb = boto3.resource('dynamodb', region_name='us-east-2')

adata = Counter([audio['id'] for audio in scan_all('audios')])
st.write('DymamoDB:', adata)

st.write('S3 audios');st.write(audio_summary())

st.write('Pacientes');st.write(scan_pats())
