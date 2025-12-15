"""Cloudflare R2 Storage Demo"""

import os
from dotenv import load_dotenv
load_dotenv()

ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID")
SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY")

r2 = None
try:
    import boto3
    if ACCOUNT_ID and ACCESS_KEY:
        r2 = boto3.client(
            's3',
            endpoint_url=f'https://{ACCOUNT_ID}.r2.cloudflarestorage.com',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )
        print("R2 initialized")
    else:
        print("Running in demo mode")
except ImportError:
    print("boto3 not installed. Demo mode.")

def list_buckets():
    print("\nList Buckets:")
    if r2:
        response = r2.list_buckets()
        for bucket in response['Buckets']:
            print(f"  {bucket['Name']}")
    else:
        print("  [Demo] assets, backups, uploads")

def workers_demo():
    print("\nWorkers Integration:")
    code = '''
// In Cloudflare Worker
export default {
  async fetch(request, env) {
    const object = await env.MY_BUCKET.get("file.jpg");
    return new Response(object.body, {
      headers: { "content-type": "image/jpeg" }
    });
  }
}
'''
    print(code)

def main():
    print("=" * 50)
    print("Cloudflare R2 Storage Demo")
    print("=" * 50)
    print("\n1. List Buckets\n2. Workers Integration")
    choice = input("Select (1-2): ").strip()
    if choice == "1": list_buckets()
    elif choice == "2": workers_demo()

if __name__ == "__main__":
    main()
