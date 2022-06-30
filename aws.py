from boto3 import client

def audio_list():
    conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
    objects = conn.list_objects(Bucket='quantcldata',Prefix='AUDIOS/AUDIO')
    files = [key['Key']  for key in objects['Contents']]
    return files

def audio_summary():
    conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
    objects = conn.list_objects(Bucket='quantcldata',Prefix='AUDIOS/AUDIO')
    users = set([obj['Key'].split('/')[-1].split('_')[1:]
                for obj in objects)

    return users
