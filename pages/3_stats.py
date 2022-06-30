import boto3, s3fs
from aws import *

import pandas as pd
import streamlit as st
from collections import Counter

def scan_all(tablename):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(tablename)
    resp = table.scan(ProjectionExpression="id, email")
    return resp['Items']

st.set_page_config(
    page_title="Estadísticas Parkinson", page_icon="⬇", layout="wide"
)

fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")
    
s3 = boto3.resource('s3', region_name='us-east-2')  # should be validated with ENV? credentials
ddb = boto3.resource('dynamodb', region_name='us-east-2')
#my_bucket = s3.Bucket('quantcldata/AUDIOS')
#s3data = my_bucket.objects.all()

#st.write('S3:', s3data)
audios = scan_all('audios')
adata = Counter([audio['id'] for audio in audios])
st.write('DymamoDB:', adata)
st.write('-'*80)

#s3_audiolist = audio_list()
s3_audiolist = audio_summary()
st.write('<H2>S3 audios</H2>')
st.write(s3_audiolist)
