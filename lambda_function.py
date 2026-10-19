import json
import urllib.parse
import boto3
from datetime import datetime

# 1. AWS-ലെ S3-ഉം DynamoDB-യുമായി കണക്ഷൻ ഉണ്ടാക്കുന്നു
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# 2. നമ്മൾ AWS-ൽ ഉണ്ടാക്കാൻ പോകുന്ന ഡാറ്റാബേസ് ടേബിളിന്റെ പേര്
TABLE_NAME = 'FileMetadataTable'
table = dynamodb.Table(TABLE_NAME)

# 3. പ്രധാന ഫംഗ്ഷൻ (S3-ൽ ഫയൽ വരുമ്പോൾ ഇത് തനിയെ റൺ ആകും)
def lambda_handler(event, context):
    try:
        # S3 തരുന്ന മെസ്സേജിൽ (event) നിന്ന് ഫയലിന്റെ വിവരങ്ങൾ എടുക്കുന്നു
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        file_key = urllib.parse.unquote_plus(record['s3']['object']['key']) # ഫയലിന്റെ പേര്
        file_size = record['s3']['object']['size'] # ഫയലിന്റെ സൈസ്
        
        # S3-ൽ നിന്ന് ഫയൽ ഏത് ടൈപ്പ് ആണെന്ന് (image/pdf/text) കണ്ടുപിടിക്കുന്നു
        response = s3_client.head_object(Bucket=bucket_name, Key=file_key)
        content_type = response.get('ContentType', 'unknown')
        
        # ഡാറ്റാബേസിൽ സേവ് ചെയ്യാനുള്ള വിവരങ്ങൾ ഒതുക്കി ഒരു ലിസ്റ്റ് ആക്കുന്നു
        item = {
            'file_id': file_key,                     # മെയിൻ ഐഡി (Partition Key)
            'bucket_name': bucket_name,             # ഏത് ബക്കറ്റിലാണ് ഉള്ളത്
            'file_size_bytes': file_size,           # ഫയൽ സൈസ്
            'content_type': content_type,           # ഫയൽ ടൈപ്പ്
            'upload_time': datetime.utcnow().isoformat(), # അപ്‌ലോഡ് ചെയ്ത സമയം
            'status': 'PROCESSED'
        }
        
        # ഈ വിവരങ്ങൾ DynamoDB ഡാറ്റാബേസിലേക്ക് എഴുതുന്നു
        table.put_item(Item=item)
        
        print(f"File processed successfully: {file_key}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success', 'file_id': file_key})
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e