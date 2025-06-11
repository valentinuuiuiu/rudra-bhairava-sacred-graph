#!/usr/bin/env python3
"""
Download test images for marketplace listings using Picsum Photos
"""
import os
import requests
import time
from urllib.parse import urlparse

# Create sample_images directory
os.makedirs('sample_images', exist_ok=True)

# Define test images with different sizes and IDs
test_images = [
    # Electronics
    {'url': 'https://picsum.photos/800/600?random=1', 'filename': 'laptop_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=2', 'filename': 'laptop_2.jpg'},
    {'url': 'https://picsum.photos/800/600?random=3', 'filename': 'phone_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=4', 'filename': 'phone_2.jpg'},
    {'url': 'https://picsum.photos/800/600?random=5', 'filename': 'tablet_1.jpg'},
    
    # Home & Garden
    {'url': 'https://picsum.photos/800/600?random=6', 'filename': 'sofa_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=7', 'filename': 'sofa_2.jpg'},
    {'url': 'https://picsum.photos/800/600?random=8', 'filename': 'chair_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=9', 'filename': 'table_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=10', 'filename': 'lamp_1.jpg'},
    
    # Fashion
    {'url': 'https://picsum.photos/800/600?random=11', 'filename': 'jacket_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=12', 'filename': 'jacket_2.jpg'},
    {'url': 'https://picsum.photos/800/600?random=13', 'filename': 'dress_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=14', 'filename': 'shoes_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=15', 'filename': 'bag_1.jpg'},
    
    # Books
    {'url': 'https://picsum.photos/800/600?random=16', 'filename': 'book_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=17', 'filename': 'book_2.jpg'},
    {'url': 'https://picsum.photos/800/600?random=18', 'filename': 'magazine_1.jpg'},
    
    # Sports
    {'url': 'https://picsum.photos/800/600?random=19', 'filename': 'bike_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=20', 'filename': 'bike_2.jpg'},
    {'url': 'https://picsum.photos/800/600?random=21', 'filename': 'equipment_1.jpg'},
    
    # Art
    {'url': 'https://picsum.photos/800/600?random=22', 'filename': 'painting_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=23', 'filename': 'sculpture_1.jpg'},
    
    # Collectibles
    {'url': 'https://picsum.photos/800/600?random=24', 'filename': 'vintage_1.jpg'},
    {'url': 'https://picsum.photos/800/600?random=25', 'filename': 'vintage_2.jpg'},
]

def download_image(url, filename):
    """Download a single image with proper error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"Downloading {filename}...")
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        # Check if we got a valid image response
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print(f"  Warning: {filename} - Content-Type is {content_type}")
        
        filepath = os.path.join('sample_images', filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Check file size
        file_size = os.path.getsize(filepath)
        if file_size < 1000:  # Less than 1KB is suspicious
            print(f"  Warning: {filename} is only {file_size} bytes")
            return False
        else:
            print(f"  Success: {filename} ({file_size:,} bytes)")
            return True
            
    except Exception as e:
        print(f"  Error downloading {filename}: {e}")
        return False

def main():
    print("Downloading test images...")
    
    successful = 0
    failed = 0
    
    for img in test_images:
        if download_image(img['url'], img['filename']):
            successful += 1
        else:
            failed += 1
        
        # Small delay to be respectful
        time.sleep(0.5)
    
    print(f"\nDownload completed:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    
    # List downloaded files
    print(f"\nDownloaded files:")
    for filename in os.listdir('sample_images'):
        if filename.endswith('.jpg'):
            filepath = os.path.join('sample_images', filename)
            size = os.path.getsize(filepath)
            print(f"  {filename}: {size:,} bytes")

if __name__ == '__main__':
    main()
