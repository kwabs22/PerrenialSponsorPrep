"""
Cloudinary Media Management Demo
Showcases: Image transforms, AI features, video processing
"""

import os
from dotenv import load_dotenv

load_dotenv()

CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

cloudinary = None
try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    from cloudinary import CloudinaryImage, CloudinaryVideo

    if CLOUDINARY_URL:
        cloudinary.config(cloudinary_url=CLOUDINARY_URL)
        print("Cloudinary initialized")
    else:
        print("Warning: CLOUDINARY_URL not set. Running in demo mode.")
        cloudinary = None
except ImportError:
    print("cloudinary not installed. Running in demo mode.")

def basic_transform_demo():
    """Basic image transformations"""
    print("\nBasic Transformations:")

    transforms = [
        ("Resize", "w_300,h_300,c_fill"),
        ("Crop to face", "w_200,h_200,c_thumb,g_face"),
        ("Round corners", "r_max"),
        ("Grayscale", "e_grayscale"),
        ("Blur", "e_blur:300"),
    ]

    print("  Transform URLs:")
    for name, transform in transforms:
        url = f"https://res.cloudinary.com/demo/image/upload/{transform}/sample.jpg"
        print(f"    {name}: {url}")

def ai_features_demo():
    """AI-powered transformations"""
    print("\nAI Features:")

    ai_transforms = [
        ("Background Removal", "e_background_removal"),
        ("Generative Fill", "c_pad,w_1000,h_1000,b_gen_fill"),
        ("Object Detection", "l_bag,fl_region_relative,g_detected:bag"),
        ("Auto Enhance", "e_auto_enhance"),
        ("Upscale", "e_upscale"),
    ]

    print("  AI Transform URLs:")
    for name, transform in ai_transforms:
        url = f"https://res.cloudinary.com/demo/image/upload/{transform}/sample.jpg"
        print(f"    {name}:")
        print(f"      {url}")

def responsive_demo():
    """Responsive image delivery"""
    print("\nResponsive Images:")

    code = '''
<!-- Responsive with automatic format -->
<img
  src="https://res.cloudinary.com/demo/image/upload/w_auto,c_scale,f_auto,q_auto/sample.jpg"
  srcset="
    https://res.cloudinary.com/demo/image/upload/w_300,c_scale,f_auto,q_auto/sample.jpg 300w,
    https://res.cloudinary.com/demo/image/upload/w_600,c_scale,f_auto,q_auto/sample.jpg 600w,
    https://res.cloudinary.com/demo/image/upload/w_1200,c_scale,f_auto,q_auto/sample.jpg 1200w
  "
  sizes="(max-width: 600px) 300px, (max-width: 1200px) 600px, 1200px"
>
'''
    print(code)

def video_demo():
    """Video transformations"""
    print("\nVideo Processing:")

    video_transforms = [
        ("Thumbnail", "so_5,c_fill,w_300,h_200"),
        ("GIF preview", "dl_200,vs_10,w_300"),
        ("Watermark", "l_logo,g_south_east,o_50"),
        ("Trim", "so_0,eo_10"),
    ]

    print("  Video Transforms:")
    for name, transform in video_transforms:
        url = f"https://res.cloudinary.com/demo/video/upload/{transform}/elephant.mp4"
        print(f"    {name}: {url}")

def upload_demo():
    """Upload with transformations"""
    print("\nUpload Demo:")

    if cloudinary:
        # Would upload a file
        print("  Upload API available")
        print("  cloudinary.uploader.upload('image.jpg', transformation=[...])")
    else:
        code = '''
import cloudinary.uploader

result = cloudinary.uploader.upload(
    "local_image.jpg",
    public_id="my_image",
    transformation=[
        {"width": 1000, "crop": "limit"},
        {"quality": "auto", "fetch_format": "auto"}
    ],
    tags=["hackathon", "demo"]
)

print(result["secure_url"])
'''
        print(code)

def main():
    print("=" * 50)
    print("Cloudinary Media Demo")
    print("=" * 50)

    print("\nAvailable demos:")
    print("  1. Basic Transformations")
    print("  2. AI Features")
    print("  3. Responsive Images")
    print("  4. Video Processing")
    print("  5. Upload API")
    print("  6. Run all")

    choice = input("\nSelect demo (1-6): ").strip()

    demos = {
        "1": basic_transform_demo,
        "2": ai_features_demo,
        "3": responsive_demo,
        "4": video_demo,
        "5": upload_demo,
    }

    if choice == "6":
        for demo in demos.values():
            demo()
    elif choice in demos:
        demos[choice]()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
