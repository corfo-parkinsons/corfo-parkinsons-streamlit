from newaudio import *
from aws import *
nau=SoundData('*.mp3')

#import boto3
ddb=boto3.resource('dynamodb')
table=ddb.Table('audio_test2')

for _,row in nau.df.iterrows():
    drow = row.to_dict()
    srow = {k: round(v,3) for k,v in drow.items() if isinstance(v,float)}
    for k, v in drow.items():
        if not isinstance(v,float):
            srow[k]=v
    for k in drow.keys():
        if 'breaks' in k:
            del srow[k]
    response=table.put_item(Item={'id':row['filename'],'data':str(srow)})

ver_tabla('audio_test2')
