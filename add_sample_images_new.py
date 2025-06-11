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

def add_sample_images():
    """Add sample images to existing listings using the downloaded test images"""
    
    # First, clean up any existing images to start fresh
    print("Cleaning up existing listing images...")
    ListingImage.objects.all().delete()
    
    # Image mappings - map listing titles to image files (using downloaded images)
    image_mappings = {
        'Bicicletă montană - Trek Marlin 7': [
            'bike_1.jpg',
            'bike_2.jpg'
        ],
        'Set mobilier grădină': [
            'sofa_1.jpg',
            'table_1.jpg',
            'chair_1.jpg'
        ],
        'Jachetă din piele designer, mărimea M': [
            'jacket_1.jpg',
            'jacket_2.jpg'
        ],
        'iPhone 13 Pro, 256GB, ca nou': [
            'phone_1.jpg',
            'phone_2.jpg'
        ],
        'BMW 320d 2018, stare excelentă': [
            'vintage_1.jpg',  # Using vintage for luxury car
            'vintage_2.jpg'
        ],
        'Apartament modern 2 camere în centrul Bucureștiului': [
            'sofa_2.jpg',  # Interior shots
            'lamp_1.jpg'
        ],
        # For service listings, we'll add some generic professional images
        'Servicii profesionale de curățenie locuințe': [
            'equipment_1.jpg'
        ],
        'Dezvoltator Software - Lucru Remote': [
            'laptop_1.jpg',
            'laptop_2.jpg'
        ]
    }
    
    sample_images_dir = '/home/shiva/Desktop/piata-ro-project/sample_images'
    
    # Get all listings
    listings = Listing.objects.all()
    print(f"Found {listings.count()} listings to add images to\n")
    
    images_added = 0
    
    for listing in listings:
        title = listing.title
        print(f"Processing listing: {title}")
        
        # Find matching images for this listing
        images_for_listing = image_mappings.get(title, [])
        
        if not images_for_listing:
            print(f"  - No images mapped for this listing")
            continue
        
        for i, image_filename in enumerate(images_for_listing):
            image_path = os.path.join(sample_images_dir, image_filename)
            
            if os.path.exists(image_path):
                try:
                    with open(image_path, 'rb') as img_file:
                        # Create ListingImage
                        listing_image = ListingImage.objects.create(
                            listing=listing,
                            is_main=(i == 0)  # First image is main
                        )
                        
                        # Save the image file
                        listing_image.image.save(
                            f"{listing.id}_{image_filename}", 
                            File(img_file), 
                            save=True
                        )
                        
                        print(f"  - Added {'main' if i == 0 else 'additional'} image: {image_filename}")
                        images_added += 1
                        
                except Exception as e:
                    print(f"  - Error adding {image_filename}: {e}")
            else:
                print(f"  - Image file not found: {image_path}")
        
        print()
    
    print(f"Successfully added {images_added} images to listings!")
    
    # Show summary
    print("\nFinal summary:")
    for listing in Listing.objects.all():
        image_count = listing.images.count()
        main_image = listing.images.filter(is_main=True).first()
        if image_count > 0:
            print(f"  - {listing.title}: {image_count} images (main: {main_image.image.name if main_image else 'None'})")
        else:
            print(f"  - {listing.title}: No images")

if __name__ == "__main__":
    add_sample_images()
