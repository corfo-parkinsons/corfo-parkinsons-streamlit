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


