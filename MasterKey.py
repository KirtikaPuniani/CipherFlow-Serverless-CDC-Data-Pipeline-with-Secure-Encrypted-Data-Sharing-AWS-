from cryptography.fernet import Fernet
import os

master_key_file = "master.key"

def get_master_key():
    if not os.path.exists(master_key_file):
        key = Fernet.generate_key()
        with open(master_key_file, "wb") as master_key:
            master_key.write(key)
    else:
        with open(master_key_file, "rb") as master_key:
            key = master_key.read()
    
    return key