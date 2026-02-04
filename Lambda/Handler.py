import boto3
import pandas as pd
import io
import os

from Crypto_Utilisation import generate_data_key, encrypt_bytes
from Merge_Utilisation import appy_cdc_merge

s3 = boto3.client('s3')

bucket = os.environ.get('cipherflow-secure-bucket')
master_key = "master/master_key.csv"
cdc_key = "encrypted/"
primary_key = "id"

def load_csv_from_s3():
    try:
        master_obj = s3.get_object(Bucket=bucket, Key=master_key)
        master_df = pd.read_csv(io.BytesIO(master_obj['Body'].read()))
        return master_df
    except s3.exceptions.NoSuchKey:
        return pd.DataFrame()

def save_csv_to_s3(df: pd.DataFrame):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=master_key, Body=csv_buffer.getvalue())
    
def lambda_handler(event, context):
    #this is triggered when new cdc csv lands in the S3 bucket
    
    #get cdc file from S3
    cdc_key = event['Records'][0]['s3']['object']['key']
    cdc_obj = s3.get_object(Bucket=bucket, Key=cdc_key)
    cdc_df = pd.read_csv(io.BytesIO(cdc_obj['Body'].read()))
    
    #load the existing master file
    existing_df = load_csv_from_s3()
    
    #applying delta and merge logic
    merged_df = appy_cdc_merge(existing_df, cdc_df, primary_key)
    
    #converting merged data to bytes
    csv_buffer = io.StringIO()
    merged_df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')
    
    #envelop encryption
    data_key, encrypted_data_key = generate_data_key()
    encrypted_bytes = encrypt_bytes(csv_bytes, data_key)
    
    #upload encrypted master file back to S3
    s3.put_object(
        Bucket=bucket,
        Key=f"{cdc_key}data_key_encrypted.bin",
        Body=encrypted_data_key,
        Metadata={
            'x-amz-meta-encrypted-data-key': encrypted_data_key.hex()
        }
    )
    
    #save the updates master file for next time
    save_csv_to_s3(merged_df)
    
    return {'statusCode': 200, 'body': 'Master file updated successfully.'}