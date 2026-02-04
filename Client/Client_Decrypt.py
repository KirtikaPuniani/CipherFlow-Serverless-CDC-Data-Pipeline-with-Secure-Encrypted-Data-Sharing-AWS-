import boto3
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

BUCKET_NAME = os.environ.get("cipherflow-secure-bucket")
REGION = os.environ.get("us-east-1")
KMS_KEY_ID = os.environ.get("KMS_KEY_ID")

if not all([BUCKET_NAME, REGION, KMS_KEY_ID]):
    raise RuntimeError("Set BUCKET_NAME, AWS_REGION, KMS_KEY_ID before running.")

# ---------- AWS Clients ----------
s3 = boto3.client("s3", region_name=REGION)
kms = boto3.client("kms", region_name=REGION)


def decrypt_data_key(encrypted_key_blob: bytes) -> bytes:
    """
    Ask KMS to decrypt the encrypted data key.
    Client IAM role must have kms:Decrypt permission.
    """
    response = kms.decrypt(CiphertextBlob=encrypted_key_blob)
    return response["Plaintext"]


def decrypt_bytes(encrypted_data: bytes, data_key: bytes) -> bytes:
    """
    Decrypt AES encrypted content.
    First 16 bytes are IV.
    """
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = Cipher(
        algorithms.AES(data_key),
        modes.CFB(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def main():
    # 1️⃣ Download encrypted files from S3
    encrypted_file = s3.get_object(
        Bucket=BUCKET_NAME,
        Key="encrypted/data_encrypted.bin"
    )["Body"].read()

    encrypted_key_blob = s3.get_object(
        Bucket=BUCKET_NAME,
        Key="encrypted/data_key_encrypted.bin"
    )["Body"].read()

    # 2️⃣ Decrypt data key via KMS
    data_key = decrypt_data_key(encrypted_key_blob)

    # 3️⃣ Decrypt CSV data
    decrypted_csv = decrypt_bytes(encrypted_file, data_key)

    # 4️⃣ Save locally
    with open("decrypted_output.csv", "wb") as f:
        f.write(decrypted_csv)

    print("✅ File decrypted successfully: decrypted_output.csv")


if __name__ == "__main__":
    main()
