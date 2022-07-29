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

def scan_all(tablename):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(tablename)
    resp = table.scan(ProjectionExpression="id, email")
    return resp['Items']

def scan_pats():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Pacientes')
    return table.scan()['Items']

import requests
def schedules():
    
    URL = 'https://quantcldata.s3.us-east-2.amazonaws.com/CLIENTES/CORFO/pacientes_test.json'
    return pd.read_json(URL)

def audio_data(all=False):
    dynamodb=boto3.resource('dynamodb')
    table=dynamodb.Table('audios')
    data=table.scan()
    print('N=', data['Count'])

    summary = Counter([di['id'] for di in data['Items']])
    adf = pd.DataFrame(data['Items'])
    #adf['time'] = eval(','.join(adf['data'].apply(dt).split(',')[:5]))
    adf['time'] = adf['data'].apply(dt)
    adf['fecha'] = adf.time.apply(lambda t: '%d-%02d-%02d' %(t[0],t[1],t[2]))
    adf['hora'] = adf.time.apply(lambda t: '%d:%02d:%02d' %(t[3],t[4],t[5]))
    print(summary)
    if all:
        return adf
    else:
        return adf[['id','time','fecha','hora']].sort_values(['fecha','hora'])

