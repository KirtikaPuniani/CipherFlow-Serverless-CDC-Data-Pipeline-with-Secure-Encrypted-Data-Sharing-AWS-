from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from KeyStorage import load_key, new_encrypt_key
from MasterKey import get_master_key

rotation_days = 45

master_fernet = Fernet(get_master_key())

def generate_dek_entry():
    dek = Fernet.generate_key()
    encrypted_key = master_fernet.encrypt(dek)
    
    return{
        "key_id": f"dek_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "creation_date": datetime.now().isoformat(),
        "encrypted_key": encrypted_key.decode(),
        "status": "active"
    }
    
def key_rotation():
    store = load_key()
    now = datetime.now()
    
    if store:
        latest = store[-1]
        creation_date = datetime.fromisoformat(latest["creation_date"])
        if now - creation_date < timedelta(days = rotation_days):
            return latest["key_id"]
        latest["status"] = "expired"
    
    new_encrypted_key = generate_dek_entry()
    new_encrypt_key(new_encrypted_key)
    return new_encrypted_key["key_id"]