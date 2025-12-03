"""
AWS Amazon Q Data Pipeline
Showcases: Amazon Q + Bedrock
"""
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Check for boto3
try:
    import boto3
    from botocore.config import Config
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

def get_bedrock_client():
    """Initialize Bedrock client."""
    config = Config(region_name=AWS_REGION)
    return boto3.client(
        "bedrock-runtime",
        config=config,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

def invoke_claude(prompt: str):
    """Invoke Claude via Bedrock."""
    client = get_bedrock_client()

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    response = client.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=body
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]

def generate_pipeline_code(description: str):
    """Generate data pipeline code using AI."""
    prompt = f"""Generate a simple AWS data pipeline for the following requirement:

{description}

Include:
1. S3 bucket setup
2. Lambda function code
3. EventBridge rule

Keep it concise and production-ready."""

    return invoke_claude(prompt)

def analyze_pipeline(pipeline_code: str):
    """Analyze pipeline code for improvements."""
    prompt = f"""Analyze this AWS data pipeline code and suggest improvements:

{pipeline_code}

Focus on:
1. Security best practices
2. Cost optimization
3. Error handling"""

    return invoke_claude(prompt)

def main():
    print("=" * 50)
    print("AWS Amazon Q Data Pipeline")
    print("=" * 50)

    if not HAS_BOTO3:
        print("\nInstall boto3: pip install boto3")
        return

    if not AWS_ACCESS_KEY:
        print("\nSetup required:")
        print("1. Create AWS account")
        print("2. Enable Amazon Bedrock in console")
        print("3. Request Claude model access")
        print("4. Create IAM credentials")
        print("5. Copy credentials to .env file")

        print("\n🤖 Amazon Q Features:")
        print("  - Code generation")
        print("  - Code transformation")
        print("  - Security scanning")
        print("  - Documentation generation")

        print("\n📊 Sample Pipeline Generation:")
        print("""
# Example: Generate ETL pipeline
prompt = "Create an ETL pipeline that:
- Reads CSV from S3
- Transforms data with Lambda
- Loads to DynamoDB"

# Amazon Q / Bedrock generates complete code
        """)

        # Demo output
        print("\n🔧 Generated Pipeline (Demo):")
        demo_pipeline = '''
import boto3
import json

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Get S3 object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Read CSV
    response = s3.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode('utf-8')

    # Transform and load
    table = dynamodb.Table('processed-data')
    for row in parse_csv(data):
        table.put_item(Item=transform(row))

    return {'statusCode': 200}
'''
        print(demo_pipeline)
        return

    print(f"\nAWS Region: {AWS_REGION}")

    # Demo: Generate pipeline
    print("\n📊 Generating data pipeline...")

    description = """
    Create a simple data pipeline that:
    1. Triggers when a file is uploaded to S3
    2. Processes the file with Lambda
    3. Stores results in DynamoDB
    """

    try:
        pipeline_code = generate_pipeline_code(description)
        print("\n🔧 Generated Pipeline:")
        print(pipeline_code[:1000])

        # Analyze
        print("\n🔍 Analyzing pipeline...")
        analysis = analyze_pipeline(pipeline_code)
        print("\n📋 Analysis:")
        print(analysis[:500])

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Bedrock and Claude are enabled in your AWS account.")

if __name__ == "__main__":
    main()
