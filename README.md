# CipherFlow-Serverless-CDC-Data-Pipeline-with-Secure-Encrypted-Data-Sharing-AWS-

**🔐 CipherFlow**
Serverless CDC Data Pipeline with Secure Encrypted Data Sharing on AWS
CipherFlow is a cloud-native, serverless Change Data Capture (CDC) pipeline built on AWS that securely processes incremental database changes and distributes encrypted data snapshots to external consumers via S3.
The system is designed with enterprise-grade security, enforcing strict producer–consumer isolation using AWS KMS asymmetric envelope encryption, ensuring the pipeline can encrypt data without ever being able to decrypt it.

**🚀 Problem Statement**
Traditional batch pipelines:
1. Reprocess entire tables weekly
2. Increase compute and storage costs
3. Lack secure mechanisms for sharing data externally
3. Expose risks with shared encryption keys

**CipherFlow solves this by using:**
1. CDC-based incremental processing
2. Serverless orchestration
3. Envelope encryption with asymmetric keys
4. IAM-enforced separation of duties

**🏗️ Architecture Overview**
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


**🔄 Pipeline Flow**
AWS DMS captures INSERT, UPDATE, DELETE events from the source database.
Lambda applies idempotent delta + merge logic to maintain an updated dataset.
Lambda generates a one-time AES data key to encrypt the CSV snapshot.
The data key is encrypted using AWS KMS asymmetric public key.
Encrypted CSV + encrypted data key are uploaded to S3.
Client IAM role uses KMS private key to decrypt the data key and access the file.

**🔐 Security Design
**Pipeline Role**	           |      **Client Role**
kms:Encrypt only	           |      kms:Decrypt only
Cannot read data	           |      Can decrypt data
No private key access        | 	    Private key access via KMS
This enforces encryption without decryption rights for the pipeline.
