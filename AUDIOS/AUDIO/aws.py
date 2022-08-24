import boto3
#from boto3.dynamodb.conditions import Key
from config import IN_FMT, OUT_FMT

s3 = boto3.client('s3')

def s3ls(bucket):
    print('bucket:', bucket)
    data = s3.list_objects(Bucket='quantcldata',Prefix=bucket)
    print('KISS:', data.keys())
    data = data['Contents']
    nFiles = len(data)

    txt = '<B>Archivo    Fecha (tamaño)</B>\n'
    txt += '-'*32+'\n'
    for d in data:
        fecha = d['LastModified'].strftime('%Y%m%d %H:%M')
        txt += '<B>%s</B> %s [%d]\n' %(d['Key'], fecha, d['Size']) 
    txt += '-'*32+'\n'
    txt += f'Procesando {nFiles} archivos\n'
    
    return txt


def register_insert(id, filename):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Users')

    table.update_item(
        Key={
                'id': id,
            },
        UpdateExpression="set first_name = :g",
        ExpressionAttributeValues={
                ':g': filename
            },
        ReturnValues="UPDATED_NEW"
        )

def upload_audio_to_s3(file_name):
    sfile_name = file_name.replace('AUDIOS/','')
    bucket = 'quantcldata'
    base_name = file_name
    for name in [base_name, base_name.replace(IN_FMT, OUT_FMT)]:
        object_name = 'AUDIOS/'+name
        print('AWS:upload_audio_to_s3 = ', object_name)
        s3.upload_file(name, bucket, object_name)

#### pacientes dynamoDB
def insertar_paciente(nombre, fecha, username):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Pacientes')
    table.put_item(Item={'nombre': nombre, 'fecha': fecha,
                         'username': username})

def insertar_medicina(nombre_paciente, medicamento, dosis, fecha):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Medicamentos')
    table.put_item(Item={'nombre': nombre_paciente, 'medicamento': medicamento,
                         'dosis': dosis, 'fecha': fecha})

def ver_tabla(tabla):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(tabla)
    return table.scan()['Items']

def ver_pacientes():    return ver_tabla('Pacientes')
def ver_medicamentos():    return ver_tabla('Medicamentos')
