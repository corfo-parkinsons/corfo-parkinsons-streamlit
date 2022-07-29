from boto3 import client
import pandas as pd

def audio_list():
    conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
    objects = conn.list_objects(Bucket='quantcldata',Prefix='AUDIOS/AUDIO')
    files = [key['Key']  for key in objects['Contents']]
    return files

def audio_summary():
    conn = client('s3')  
    objects = conn.list_objects(Bucket='quantcldata',Prefix='AUDIOS/AUDIO')

    cdf = pd.DataFrame(objects['Contents'])
    cdf['user'] = cdf.Key.apply(lambda k: k.split('/')[-1].split('_')[1:][0])


    return cdf.user.value_counts()
#############
import boto3, s3fs
import pandas as pd
from collections import Counter

def ddb():
    return boto3.resource('dynamodb', region_name='us-east-2')
def scan_all(tablename):
    dynamodb = ddb()
    table = dynamodb.Table(tablename)
    resp = table.scan(ProjectionExpression="id, email")
    return resp['Items']

def scan_pats():
    dynamodb = ddb()
    table = dynamodb.Table('Pacientes')
    return table.scan()['Items']

import requests
def schedules():
    
    URL = 'https://quantcldata.s3.us-east-2.amazonaws.com/CLIENTES/CORFO/pacientes_test.json'
    return pd.read_json(URL)

def dt(di):   
    ts = di.split('"')[0].split('(')[2].split(',')[:6]
    return [int(t) for t in ts]

def freqs(d):
    # {'JOMAX Contacto': (5221716593, datetime.datetime(2022, 7, 29, 22, 1, 9, tzinfo=<UTC>), 
    #  "{'F0': '193 [M=(100,165), F=(190,262)]', 'F0dev': 16.9653, 'hnr': '20 [16.5, 20]', 
    #    'nhr': '0.014 [0.11, 0.19]', 'localJit': 0.0044, 'localabsoluteJitter': 2e-05, 
    #    'rapJitter': 0.00255, 'ppq5Jitter': 0.0026, 'ddpJitter': 0.00766, 'localShimmer': 0.03913, 
    #    'localdbShimmer': 0.33881, 'apq3Shimmer': 0.02202, 'aqpq5Shimmer': 0.02408, 'apq11Shimmer': 0.02804, 
    #    'ddaShimmer': 0.06607, 'intensity': '72 [55,80]', 'PPE': 0.0003, 'Parkinson': '87.2%', 'F1': '601 [M=(718,906), F=(430,970)]', 
    #    'F2': '1284 [M=(1160,1300), F=(1380,1820)]', 'F3': '2247 [M=(2520,3020), F=(2750,3250)]', 'F4': '3431 [M=(3700,4250), F=(4050,4550)]', 
    #    'F2/F1': '2.140 [a=1.6,e=3.4,6.8,2.4]'}")}
    ds = d[1:700]
    cuts1 = [ds.index(toke) for toke in ["'F0'","'F1'","'F2'","'F3'","'F4'",]]
    cuts2 = [ds[cut:].split("'")[3].split(' ')[0] for cut in cuts1]    #  'F1': '815 
    return cuts2

def audio_data(all=False):
    dynamodb = ddb()
    table=dynamodb.Table('audios')
    data=table.scan()
    print('N=', data['Count'])

    summary = Counter([di['id'] for di in data['Items']])
    adf = pd.DataFrame(data['Items'])
    adf['time'] = adf['data'].apply(dt)
    adf['fecha'] = adf.time.apply(lambda t: '%d-%02d-%02d' %(t[0],t[1],t[2]))
    adf['hora'] = adf.time.apply(lambda t: '%d:%02d:%02d' %(t[3],t[4],t[5]))
    adf['coefs'] = adf['data'].apply(freqs)
    #print(summary)
    if all:
        return adf[['id','fecha','hora','coefs']]
    else:
        return adf[['id','time','fecha','hora']].sort_values(['fecha','hora'])

