"""Uploadcare File Upload Demo"""

import os
from dotenv import load_dotenv
load_dotenv()

PUBLIC_KEY = os.getenv("UPLOADCARE_PUBLIC_KEY", "demopublickey")

def widget_demo():
    print("\nUpload Widget:")
    code = f'''
<script src="https://ucarecdn.com/libs/widget/3.x/uploadcare.full.min.js"></script>
<input type="hidden" role="uploadcare-uploader" data-public-key="{PUBLIC_KEY}" />
'''
    print(code)

def transform_demo():
    print("\nTransformations:")
    uuid = "demo-uuid"
    transforms = [
        ("Resize", f"https://ucarecdn.com/{uuid}/-/resize/300x300/"),
        ("Crop", f"https://ucarecdn.com/{uuid}/-/crop/16:9/"),
        ("WebP", f"https://ucarecdn.com/{uuid}/-/format/webp/"),
    ]
    for name, url in transforms:
        print(f"  {name}: {url}")

def main():
    print("=" * 50)
    print("Uploadcare Demo")
    print("=" * 50)
    print("\n1. Widget\n2. Transforms")
    choice = input("Select (1-2): ").strip()
    if choice == "1": widget_demo()
    elif choice == "2": transform_demo()

if __name__ == "__main__":
    main()
