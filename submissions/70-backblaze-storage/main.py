"""Backblaze B2 Storage Demo"""

import os
from dotenv import load_dotenv
load_dotenv()

KEY_ID = os.getenv("B2_KEY_ID")
APP_KEY = os.getenv("B2_APPLICATION_KEY")

b2 = None
try:
    import boto3
    if KEY_ID and APP_KEY:
        b2 = boto3.client(
            's3',
            endpoint_url='https://s3.us-west-004.backblazeb2.com',
            aws_access_key_id=KEY_ID,
            aws_secret_access_key=APP_KEY
        )
        print("B2 initialized (S3 compatible)")
    else:
        print("Running in demo mode")
except ImportError:
    print("boto3 not installed. Demo mode.")

def list_buckets():
    print("\nList Buckets:")
    if b2:
        response = b2.list_buckets()
        for bucket in response['Buckets']:
            print(f"  {bucket['Name']}")
    else:
        print("  [Demo] my-bucket-1, my-bucket-2")

def upload_demo():
    print("\nUpload Demo:")
    code = '''
b2.upload_file(
    Bucket='my-bucket',
    Key='path/to/file.jpg',
    Body=open('file.jpg', 'rb')
)
'''
    print(code)

def main():
    print("=" * 50)
    print("Backblaze B2 Storage Demo")
    print("=" * 50)
    print("\n1. List Buckets\n2. Upload Example")
    choice = input("Select (1-2): ").strip()
    if choice == "1": list_buckets()
    elif choice == "2": upload_demo()

if __name__ == "__main__":
    main()
