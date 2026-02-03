from cryptography.fernet import Fernet
import os
import json
from MasterKey import get_master_key

key_file = 'keys.enc.json'

master_fernet = Fernet(get_master_key())

def load_key():
    if not os.path.exists(key_file):
        return[]
    with open(key_file, "rb") as key_storage:
        encrypted = key_storage.read()
    
    decrypted = master_fernet.decrypt(encrypted)
    return json.loads(decrypted)

def save_key(data):
    encrypted = master_fernet.encrypt(json.dumps(data).encode())
    with open(key_file, "wb") as key_storage:
        key_storage.write(encrypted)
    
def new_encrypt_key(entry):  #this stores a new data encryption key -- symmetric key to encrypt the data
    store = load_key()
    store.append(entry)
    save_key(store)

def get_encrypt_key(key_id):
    store = load_key()
    
    for entry in store:
        if entry["key_id"] == key_id:
            return entry
    
    raise ValueError("Key ID not found")