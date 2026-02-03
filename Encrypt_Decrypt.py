from cryptography.fernet import Fernet
from KeyRotation import key_rotation
from KeyStorage import get_encrypt_key
from MasterKey import get_master_key

master_fernet = Fernet(get_master_key())

def get_def(key_id):
    entry = get_encrypt_key(key_id)
    encrypted_dek = entry["encrypted_key"].encode()
    return master_fernet.decrypt(encrypted_dek)

#encrypting data using the data encryption key
key_id = key_rotation()
dek = get_def(key_id)
data_fernet = Fernet(dek)
cipher_text = data_fernet.encrypt(b"Highly Sensitive Data")

#decrypting data using the data encryption key
plain_text = data_fernet.decrypt(cipher_text)
print(plain_text.decode())

payload = {
    "key_id": key_id,
    "ciphertext": cipher_text.decode(),
    "plain_text": plain_text.decode()
}
print(payload)