# Serverless Event-Driven File Processing Pipeline

An automated, serverless event-driven metadata extraction pipeline built on AWS using Python and Boto3.

## Architecture Flow
1. **Amazon S3**: Acts as the object storage locker where users upload files.
2. **S3 Event Trigger**: S3 fires an `ObjectCreated` event upon successful file upload.
3. **AWS Lambda**: Serverless Python function triggered automatically to process the event, extracting file attributes (Key, Size, Content-Type, Upload Timestamp).
4. **Amazon DynamoDB**: NoSQL database that stores the parsed file metadata records.
5. **AWS IAM**: Least privilege execution roles granting Lambda secure read access to S3 and write access to DynamoDB.

## Tech Stack
- **Cloud Provider**: Amazon Web Services (AWS)
- **Compute**: AWS Lambda (Serverless Python 3.12)
- **Storage**: Amazon S3
- **Database**: Amazon DynamoDB (NoSQL)
- **SDK**: Boto3 (AWS SDK for Python)

## Deployment Steps
1. Create a DynamoDB table named `FileMetadataTable` with `file_id` (String) as Partition Key.
2. Create an S3 Bucket and enable event notifications for Lambda.
3. Create an IAM Role with `AWSLambdaBasicExecutionRole`, `AmazonS3ReadOnlyAccess`, and `AmazonDynamoDBFullAccess`.
4. Deploy `lambda_function.py` to AWS Lambda and configure the S3 trigger.