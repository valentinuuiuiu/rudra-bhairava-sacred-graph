#!/usr/bin/env python3
"""
Quick Google Maps API diagnosis script
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_apis():
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    print(f"🔑 Using API Key: {api_key[:10]}...{api_key[-4:]}")
    print()
    
    # Test different Google APIs
    tests = [
        {
            "name": "Geocoding API",
            "url": "https://maps.googleapis.com/maps/api/geocode/json",
            "params": {"address": "Test", "key": api_key},
            "required": "Essential for address lookup"
        },
        {
            "name": "Places API (Text Search)",
            "url": "https://maps.googleapis.com/maps/api/place/textsearch/json",
            "params": {"query": "Test", "key": api_key},
            "required": "Optional for enhanced place details"
        },
        {
            "name": "Places API (Nearby Search)",
            "url": "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            "params": {"location": "44.4268,26.1025", "radius": "1000", "key": api_key},
            "required": "Optional for nearby places"
        }
    ]
    
    for test in tests:
        print(f"🧪 Testing {test['name']}...")
        try:
            response = requests.get(test["url"], params=test["params"], timeout=5)
            data = response.json()
            
            status = data.get('status', 'UNKNOWN')
            
            if status == 'OK':
                print(f"   ✅ {test['name']}: ENABLED")
            elif status == 'ZERO_RESULTS':
                print(f"   ✅ {test['name']}: ENABLED (no results for test query)")
            elif status == 'REQUEST_DENIED':
                error_msg = data.get('error_message', 'API not enabled')
                print(f"   ❌ {test['name']}: DISABLED - {error_msg}")
                print(f"   📝 {test['required']}")
            elif status == 'INVALID_REQUEST':
                print(f"   ⚠️  {test['name']}: ENABLED (invalid test request)")
            else:
                print(f"   ❓ {test['name']}: {status}")
                if 'error_message' in data:
                    print(f"      Error: {data['error_message']}")
                    
        except Exception as e:
            print(f"   ❌ {test['name']}: Error - {e}")
        
        print()

if __name__ == "__main__":
    print("🔍 Google Maps API Diagnosis")
    print("=" * 40)
    test_apis()
    
    print("📋 To enable required APIs:")
    print("1. Go to: https://console.cloud.google.com/apis/library")
    print("2. Search and enable these APIs:")
    print("   - Geocoding API (REQUIRED)")
    print("   - Places API (OPTIONAL)")
    print("   - Maps JavaScript API (for frontend)")
    print("3. Wait 1-2 minutes for activation")
    print("4. Re-run this test")
