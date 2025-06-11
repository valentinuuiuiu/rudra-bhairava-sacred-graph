#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('/home/shiva/Desktop/piata-ro-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'piata_ro.settings')
django.setup()

from marketplace.models import Listing, ListingImage
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil

def add_sample_images():
    """Add sample images to existing listings"""
    
    # Clear existing images first
    ListingImage.objects.all().delete()
    
    # Get listings
    listings = Listing.objects.all()
    
    # Define image sets for different listings
    image_sets = [
        # Bikes
        ['bike_1.jpg', 'bike_2.jpg'],
        # Furniture/Home
        ['sofa_1.jpg', 'sofa_2.jpg', 'table_1.jpg'],
        # Fashion
        ['jacket_1.jpg', 'jacket_2.jpg'],
        # Electronics
        ['laptop_1.jpg', 'laptop_2.jpg'],
        # Phones
        ['phone_1.jpg', 'phone_2.jpg'],
        # Books/Media
        ['book_1.jpg', 'book_2.jpg'],
        # Art
        ['painting_1.jpg', 'sculpture_1.jpg'],
        # More items
        ['chair_1.jpg', 'lamp_1.jpg'],
    ]
    
    for i, listing in enumerate(listings):
        print(f"Adding images to: {listing.title}")
        
        # Get appropriate image set (cycle through if more listings than sets)
        image_set = image_sets[i % len(image_sets)]
        
        for j, img_name in enumerate(image_set):
            img_path = f'/home/shiva/Desktop/piata-ro-project/sample_images/{img_name}'
            
            if os.path.exists(img_path):
                with open(img_path, 'rb') as img_file:
                    # Create ListingImage
                    listing_image = ListingImage.objects.create(
                        listing=listing,
                        is_main=(j == 0)  # First image is main
                    )
                    listing_image.image.save(img_name, File(img_file), save=True)
                    image_type = "primary" if j == 0 else "additional"
                    print(f"  - Added {image_type} image: {img_name}")
            else:
                print(f"  - Image not found: {img_path}")
    
    print("\nSample images added successfully!")
    
    # Show summary
    print("\nListings with images:")
    for listing in Listing.objects.all():
        image_count = ListingImage.objects.filter(listing=listing).count()
        if image_count > 0:
            print(f"  - {listing.title}: {image_count} images")

if __name__ == "__main__":
    add_sample_images()
