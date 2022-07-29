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
    print(summary)
    if all:
        return adf
    else:
        return adf[['id','time','fecha','hora']].sort_values(['fecha','hora'])

