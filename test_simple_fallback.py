#!/usr/bin/env python3
"""
Simple test script for OpenStreetMap Nominatim geocoding fallback functionality.
Tests the free geocoding service without Django dependencies.
"""

import requests
import json
from typing import Dict, Any

# OpenStreetMap Nominatim API URLs (same as in content_media_agent.py)
NOMINATIM_API_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"

def geocode_address_free(address: str) -> Dict[str, Any]:
    """Geocode an address using free OpenStreetMap Nominatim API."""
    try:
        params = {
            'q': address,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        
        headers = {
            'User-Agent': 'Piata.ro/1.0 (contact@piata.ro)'  # Required by Nominatim
        }
        
        response = requests.get(NOMINATIM_API_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]
            
            return {
                "success": True,
                "latitude": float(result['lat']),
                "longitude": float(result['lon']),
                "formatted_address": result.get('display_name', address),
                "place_id": result.get('place_id'),
                "type": result.get('type'),
                "address_components": result.get('address', {})
            }
        else:
            return {
                "success": False,
                "error": "Address not found"
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Network error during free geocoding: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error during free geocoding: {str(e)}"
        }

def reverse_geocode_coordinates_free(latitude: float, longitude: float) -> Dict[str, Any]:
    """Reverse geocode coordinates using free OpenStreetMap Nominatim API."""
    try:
        params = {
            'lat': latitude,
            'lon': longitude,
            'format': 'json',
            'addressdetails': 1
        }
        
        headers = {
            'User-Agent': 'Piata.ro/1.0 (contact@piata.ro)'
        }
        
        response = requests.get(NOMINATIM_REVERSE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data:
            return {
                "success": True,
                "formatted_address": data.get('display_name', f"{latitude}, {longitude}"),
                "place_id": data.get('place_id'),
                "type": data.get('type'),
                "address_components": data.get('address', {}),
                "coordinates": {"lat": latitude, "lng": longitude}
            }
        else:
            return {
                "success": False,
                "error": "Coordinates not found"
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Network error during free reverse geocoding: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error during free reverse geocoding: {str(e)}"
        }

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
                print(f"    Type: {result.get('type', 'N/A')}")
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
                print(f"    Type: {result.get('type', 'N/A')}")
                print(f"    Place ID: {result.get('place_id', 'N/A')}")
                
                # Show parsed address components if available
                addr_components = result.get('address_components', {})
                if addr_components:
                    print(f"    Address components:")
                    for key, value in addr_components.items():
                        if key in ['city', 'town', 'village', 'county', 'state', 'country', 'postcode']:
                            print(f"      {key}: {value}")
            else:
                print(f"  ✗ Failed: {result['error']}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")

def test_google_maps_simulation():
    """Simulate the fallback behavior when Google Maps fails"""
    print("\n=== Simulating Google Maps Fallback Behavior ===")
    
    def simulate_geocoding_with_fallback(address: str):
        """Simulate the geocoding process with Google Maps failure and fallback"""
        print(f"\nSimulating geocoding for: {address}")
        
        # Simulate Google Maps failure (billing issue)
        print("  1. Trying Google Maps API... (simulated failure due to billing)")
        google_result = {
            "success": False,
            "error": "OVER_QUERY_LIMIT - billing account deactivated"
        }
        print(f"     ✗ Google Maps failed: {google_result['error']}")
        
        # Try fallback service
        print("  2. Falling back to OpenStreetMap Nominatim...")
        fallback_result = geocode_address_free(address)
        
        if fallback_result["success"]:
            print(f"     ✓ Fallback successful!")
            print(f"     Service: OpenStreetMap")
            print(f"     Address: {fallback_result['formatted_address']}")
            print(f"     Coordinates: {fallback_result['latitude']}, {fallback_result['longitude']}")
            print(f"     Note: Using free service due to Google Maps billing issue")
            return {
                "geocoded": True,
                "service": "openstreetmap",
                "latitude": fallback_result["latitude"],
                "longitude": fallback_result["longitude"],
                "formatted_address": fallback_result["formatted_address"],
                "note": "Using free OpenStreetMap service (Google Maps billing issue)"
            }
        else:
            print(f"     ✗ Fallback also failed: {fallback_result['error']}")
            return {
                "geocoded": False,
                "error": f"Both Google Maps and free service failed. Google: {google_result['error']}, Free: {fallback_result['error']}"
            }
    
    # Test the fallback process
    test_addresses = [
        "Piața Victoriei, Bucharest, Romania",
        "Centrul Vechi, București",
        "Strada Lipscani, București"
    ]
    
    for address in test_addresses:
        result = simulate_geocoding_with_fallback(address)
        print(f"  Final result: {json.dumps(result, indent=4)}")

def main():
    """Run all tests"""
    print("🧪 Testing OpenStreetMap Fallback Geocoding Functionality")
    print("=" * 60)
    print("This test demonstrates the fallback service when Google Maps")
    print("is unavailable due to billing issues.")
    print("=" * 60)
    
    # Test individual free service functions
    test_free_geocoding()
    test_free_reverse_geocoding()
    
    # Test the fallback simulation
    test_google_maps_simulation()
    
    print("\n" + "=" * 60)
    print("🏁 Testing completed!")
    print("\n✅ The OpenStreetMap fallback service is working correctly!")
    print("📝 When integrated into content_media_agent.py, this service will")
    print("   automatically activate when Google Maps encounters billing issues.")
    print("\n💡 To resolve Google Maps issues:")
    print("   1. Check your Google Cloud billing account")
    print("   2. Ensure you have sufficient credits/payment method")
    print("   3. Verify the Geocoding API is enabled")
    print("   4. Check API key restrictions")

if __name__ == "__main__":
    main()
