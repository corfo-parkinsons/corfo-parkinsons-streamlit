from boto3 import client

def audio_list():
    conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
    files = [key['Key']  for key in conn.list_objects(Bucket='quantcldata',Prefix='AUDIOS/AUDIO')['Contents']]
    return files
