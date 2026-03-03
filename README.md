# 🔐 CipherFlow

### Serverless CDC Data Pipeline with Secure Encrypted Data Sharing on AWS

CipherFlow is a **cloud-native, serverless Change Data Capture (CDC) pipeline** that processes incremental database changes and securely distributes **encrypted data snapshots** to external consumers via Amazon S3.

The system is built with **enterprise-grade security**, enforcing strict **producer–consumer isolation** using **AWS KMS asymmetric envelope encryption** — allowing the pipeline to encrypt data **without any ability to decrypt it**.











---

## 🚀 Problem Statement

Traditional batch pipelines:

- Reprocess entire tables weekly
- Increase compute and storage costs
- Lack secure mechanisms for sharing data externally
- Expose risks through shared encryption keys

---

## ✅ CipherFlow Solution

CipherFlow addresses these problems using:

- CDC-based incremental data processing
- Serverless event-driven architecture
- Envelope encryption with asymmetric KMS keys
- IAM-enforced separation of duties

---

## 🏗️ Architecture Overview

      Database (PostgreSQL)
              │
              ▼
      AWS DMS (CDC Stream)
              │
              ▼
      AWS Lambda (Merge + Encrypt)
              │
              ▼
          Amazon S3
              │
              ▼
      Client (KMS Decrypt)


   <img width="1536" height="1024" alt="Serverless CDC Pipeline on AWS" src="https://github.com/user-attachments/assets/3a087803-94a6-43a2-9d56-39cdbc4e95a5" />


---

## 🔄 Pipeline Flow

1. **AWS DMS** captures INSERT, UPDATE, DELETE events from the source PostgreSQL database.
2. **AWS Lambda** applies idempotent delta + merge logic to maintain the latest dataset.
3. Lambda generates a **one-time AES data key** to encrypt the CSV snapshot.
4. The data key is encrypted using the **client’s KMS public key**.
5. Encrypted CSV and encrypted data key are uploaded to S3.
6. Client IAM role uses **KMS private key access** to decrypt and consume the file.

---

## 🔐 Security Design (Key Highlights)

|      Pipeline Role    |        Client Role         |
|-----------------------|----------------------------|
| `kms:Encrypt` only    | `kms:Decrypt` only         |
| Cannot read data      | Can decrypt data           |
| No private key access | Private key access via KMS |

_> This ensures encryption without decryption capability for the pipeline._

### Why Not Fernet or PGP?

- **Fernet** → Symmetric key, violates separation of duties
- **PGP** → Manual key management, poor IAM/audit integration
- **AWS KMS** → HSM-backed keys, IAM control, audit logs, automated rotation

---

## 🧠 Key Concepts Implemented

- Change Data Capture (CDC)
- Idempotent merge logic
- Envelope encryption
- Asymmetric key cryptography
- Serverless architecture
- Least-privilege IAM design

---

## 📊 Impact & Metrics

- Processes **100K+ weekly change events**
- **<30 seconds** end-to-end latency
- **~60% reduction** in compute and storage costs
- **~70% reduction** in data transfer volume
- **99.95% pipeline availability**
- Zero shared encryption keys

---

## 🛠️ Tech Stack

- AWS Lambda
- AWS DMS
- Amazon S3
- AWS KMS (Asymmetric Keys)
- Python (Pandas, Boto3, Cryptography)
- IAM, CloudWatch
