#!/usr/bin/env python3
"""
Test script for fallback geocoding functionality in content_media_agent.py
Tests the OpenStreetMap Nominatim fallback when Google Maps is unavailable.
"""

import sys
import os
import json
import asyncio
from typing import Dict, Any

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from the content_media_agent
try:
    # Try importing from the awesome-mcp-servers directory
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'awesome-mcp-servers'))
    from content_media_agent import (
        geocode_address_free,
        reverse_geocode_coordinates_free,
        process_location,
        LocationRequest
    )
    print("✓ Successfully imported functions from content_media_agent")
except ImportError as e:
    print(f"✗ Failed to import functions: {e}")
    sys.exit(1)

def test_free_geocoding():
    """Test the free OpenStreetMap geocoding functionality"""
    print("\n=== Testing Free Geocoding Service ===")
    
    # Test addresses for Romania
    test_addresses = [
        "Bucharest, Romania",
        "Cluj-Napoca, Romania", 
        "Strada Victoriei 1, Bucharest, Romania",
        "Piața Obor, Bucharest",
        "Universitatea București, România"
    ]
    
    for address in test_addresses:
        print(f"\nTesting geocoding for: {address}")
        try:
            result = geocode_address_free(address)
            if result["success"]:
                print(f"  ✓ Success: {result['formatted_address']}")
                print(f"    Coordinates: {result['latitude']}, {result['longitude']}")
                print(f"    Place ID: {result.get('place_id', 'N/A')}")
            else:
                print(f"  ✗ Failed: {result['error']}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")

def test_free_reverse_geocoding():
    """Test the free OpenStreetMap reverse geocoding functionality"""
    print("\n=== Testing Free Reverse Geocoding Service ===")
    
    # Test coordinates for Romania
    test_coordinates = [
        (44.4268, 26.1025),  # Bucharest center
        (46.7712, 23.6236),  # Cluj-Napoca center
        (45.7494, 21.2272),  # Timișoara center
        (47.1585, 27.6014),  # Iași center
        (44.1598, 28.6348),  # Constanța center
    ]
    
    for lat, lng in test_coordinates:
        print(f"\nTesting reverse geocoding for: {lat}, {lng}")
        try:
            result = reverse_geocode_coordinates_free(lat, lng)
            if result["success"]:
                print(f"  ✓ Success: {result['formatted_address']}")
                print(f"    Place ID: {result.get('place_id', 'N/A')}")
                print(f"    Type: {result.get('type', 'N/A')}")
            else:
                print(f"  ✗ Failed: {result['error']}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")

def test_process_location_fallback():
    """Test the process_location function with fallback functionality"""
    print("\n=== Testing Process Location with Fallback ===")
    
    # Test geocoding through process_location
    print("\n--- Testing Geocoding ---")
    geocode_request = LocationRequest(
        operation="geocode",
        address="Piața Victoriei, Bucharest, Romania"
    )
    
    try:
        result = process_location(geocode_request)
        print(f"Geocoding result: {json.dumps(result, indent=2)}")
        
        if result.get("geocoded"):
            print(f"✓ Geocoding successful using {result.get('service', 'unknown')} service")
            print(f"  Address: {result.get('formatted_address')}")
            print(f"  Coordinates: {result.get('latitude')}, {result.get('longitude')}")
            if result.get('note'):
                print(f"  Note: {result['note']}")
        else:
            print(f"✗ Geocoding failed: {result.get('error')}")
    except Exception as e:
        print(f"✗ Exception during geocoding: {e}")
    
    # Test reverse geocoding through process_location
    print("\n--- Testing Reverse Geocoding ---")
    reverse_request = LocationRequest(
        operation="reverse_geocode",
        latitude=44.4368,  # Bucharest Old Town
        longitude=26.1025
    )
    
    try:
        result = process_location(reverse_request)
        print(f"Reverse geocoding result: {json.dumps(result, indent=2)}")
        
        if result.get("reverse_geocoded"):
            print(f"✓ Reverse geocoding successful using {result.get('service', 'unknown')} service")
            print(f"  Address: {result.get('formatted_address')}")
            print(f"  Coordinates: {result.get('coordinates')}")
            if result.get('note'):
                print(f"  Note: {result['note']}")
        else:
            print(f"✗ Reverse geocoding failed: {result.get('error')}")
    except Exception as e:
        print(f"✗ Exception during reverse geocoding: {e}")

def test_coordinate_validation():
    """Test coordinate validation functionality"""
    print("\n=== Testing Coordinate Validation ===")
    
    test_cases = [
        (44.4268, 26.1025, True),   # Valid Bucharest coordinates
        (91.0, 26.1025, False),     # Invalid latitude (too high)
        (44.4268, 181.0, False),    # Invalid longitude (too high)
        (-91.0, 26.1025, False),    # Invalid latitude (too low)
        (44.4268, -181.0, False),   # Invalid longitude (too low)
        (0.0, 0.0, True),           # Valid edge case
    ]
    
    for lat, lng, expected_valid in test_cases:
        validation_request = LocationRequest(
            operation="validate",
            latitude=lat,
            longitude=lng
        )
        
        try:
            result = process_location(validation_request)
            is_valid = result.get("valid", False)
            status = "✓" if is_valid == expected_valid else "✗"
            print(f"{status} Coordinates ({lat}, {lng}): valid={is_valid} (expected={expected_valid})")
            
            if not is_valid and result.get("errors"):
                print(f"    Errors: {result['errors']}")
                
        except Exception as e:
            print(f"✗ Exception validating ({lat}, {lng}): {e}")

def test_distance_calculation():
    """Test distance calculation functionality"""
    print("\n=== Testing Distance Calculation ===")
    
    # Test distance between major Romanian cities
    test_cases = [
        # (lat1, lng1, lat2, lng2, expected_distance_km_approx, city_pair)
        (44.4268, 26.1025, 46.7712, 23.6236, 318, "Bucharest to Cluj-Napoca"),
        (44.4268, 26.1025, 45.7494, 21.2272, 423, "Bucharest to Timișoara"),
        (44.4268, 26.1025, 47.1585, 27.6014, 350, "Bucharest to Iași"),
        (46.7712, 23.6236, 45.7494, 21.2272, 260, "Cluj-Napoca to Timișoara"),
    ]
    
    for lat1, lng1, lat2, lng2, expected_km, description in test_cases:
        distance_request = LocationRequest(
            operation="distance",
            latitude=lat1,
            longitude=lng1,
            target_lat=lat2,
            target_lng=lng2
        )
        
        try:
            result = process_location(distance_request)
            if "distance_km" in result:
                actual_km = result["distance_km"]
                distance_miles = result["distance_miles"]
                
                # Allow 10% tolerance for distance calculations
                tolerance = expected_km * 0.1
                is_accurate = abs(actual_km - expected_km) <= tolerance
                
                status = "✓" if is_accurate else "✗"
                print(f"{status} {description}: {actual_km} km ({distance_miles} miles)")
                print(f"    Expected: ~{expected_km} km, Difference: {abs(actual_km - expected_km):.1f} km")
            else:
                print(f"✗ {description}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"✗ Exception calculating distance for {description}: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing Fallback Geocoding Functionality")
    print("=" * 50)
    
    # Test individual free service functions
    test_free_geocoding()
    test_free_reverse_geocoding()
    
    # Test the full process_location function with fallback
    test_process_location_fallback()
    
    # Test other location features
    test_coordinate_validation()
    test_distance_calculation()
    
    print("\n" + "=" * 50)
    print("🏁 Testing completed!")
    print("\nNote: If Google Maps API shows billing issues, the fallback")
    print("OpenStreetMap service should be used automatically.")

if __name__ == "__main__":
    main()
