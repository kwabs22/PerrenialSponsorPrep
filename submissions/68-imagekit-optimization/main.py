"""ImageKit Image Optimization Demo"""

import os
from dotenv import load_dotenv
load_dotenv()

IMAGEKIT_URL = os.getenv("IMAGEKIT_URL_ENDPOINT", "https://ik.imagekit.io/demo")

def transform_demo():
    print("\nTransformations:")
    transforms = [
        ("Resize", "tr:w-300,h-300"),
        ("Smart Crop", "tr:w-300,h-300,fo-auto"),
        ("Blur", "tr:bl-10"),
        ("Quality", "tr:q-60"),
        ("Format", "tr:f-webp"),
    ]
    for name, tr in transforms:
        print(f"  {name}: {IMAGEKIT_URL}/{tr}/sample.jpg")

def ai_demo():
    print("\nAI Features:")
    print(f"  Background Removal: {IMAGEKIT_URL}/tr:e-removebg/sample.jpg")
    print(f"  Smart Crop: {IMAGEKIT_URL}/tr:w-200,h-200,fo-face/sample.jpg")

def main():
    print("=" * 50)
    print("ImageKit Optimization Demo")
    print("=" * 50)
    print("\n1. Transformations\n2. AI Features")
    choice = input("\nSelect (1-2): ").strip()
    if choice == "1": transform_demo()
    elif choice == "2": ai_demo()

if __name__ == "__main__":
    main()
