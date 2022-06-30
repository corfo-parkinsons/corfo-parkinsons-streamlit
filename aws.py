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
    cdf['user'] = cdf.Key.apply(lambnda k: k.split('/')[-1].split('_')[1:])


    return cdf
