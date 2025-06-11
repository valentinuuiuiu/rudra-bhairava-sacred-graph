#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'piata_ro.settings')
django.setup()

from marketplace.models import Listing

print("=== LISTING COORDINATES DEBUG ===")
print()

listings_with_coords = 0
listings_without_coords = 0

for listing in Listing.objects.all():
    has_coords = listing.latitude is not None and listing.longitude is not None
    if has_coords:
        listings_with_coords += 1
        print(f"✓ Listing {listing.pk}: {listing.title[:50]}...")
        print(f"  Coordinates: {listing.latitude}, {listing.longitude}")
    else:
        listings_without_coords += 1
        print(f"✗ Listing {listing.pk}: {listing.title[:50]}...")
        print(f"  No coordinates")
    print()

print(f"SUMMARY:")
print(f"Listings with coordinates: {listings_with_coords}")
print(f"Listings without coordinates: {listings_without_coords}")
print(f"Total listings: {listings_with_coords + listings_without_coords}")
