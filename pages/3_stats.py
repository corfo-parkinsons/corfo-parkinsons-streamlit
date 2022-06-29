import boto3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Estadísticas Parkinson", page_icon="⬇", layout="wide"
)

s3 = boto3.resource('s3', region='us-east-2')  # should be validated with ENV? credentials
ddb = boto3.resource('dynamodb')

st.write('S3:', s3)
st.write('DymamoDB:', ddb)
