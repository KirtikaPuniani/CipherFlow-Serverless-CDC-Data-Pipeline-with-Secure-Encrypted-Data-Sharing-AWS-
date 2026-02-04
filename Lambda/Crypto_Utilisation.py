import boto3
import os
import secrets

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

REGION = os.getenv('AWS_REGION', 'us-east-1')
kms = boto3.client('kms', region_name = REGION)
KMS_KEY_ID = os.getenv('KMS_KEY_ID')

def generate_data_key():
    '''
    ask KMS to generate a one-time AES-256 data key.
    return the plaintext key and the encrypted key blob.
    '''
    
    response = kms.generate_data_key(
        KeyId=KMS_KEY_ID,
        KeySpec='AES_256'
    )
    plaintext_key = response['Plaintext']
    encrypted_key = response['CiphertextBlob']
    return plaintext_key, encrypted_key

def encrypt_bytes(data: bytes, data_key: bytes) -> bytes:
    #encrypt bytes using AES-256 in CFB mode
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(data_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = iv + encryptor.update(data) + encryptor.finalize()
    return ciphertext