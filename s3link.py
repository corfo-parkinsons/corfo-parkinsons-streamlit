import os

def user_oggs(user='sergio_lucero'):
    oggs=os.popen('aws s3 ls s3://quantcldata/AUDIOS/AUDIO/').read().split(chr(10))
    oggs=[ogg for ogg in oggs if user in ogg]
    dtsf=[ogg.split(' ') for ogg in oggs]
    dtsf=[[dd for dd in d if len(dd)] for d in dtsf]
    #print(dtsf[:5])
    return dtsf
