#!/usr/bin/env python3
"""
Test Google Maps Integration for Content Media Agent
Run this script to test Google Maps API functionality
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_maps_api():
    """Test Google Maps API directly"""
    print("🗺️  Testing Google Maps API Integration")
    print("=" * 50)
    
    # Check if API key is configured
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("❌ GOOGLE_MAPS_API_KEY not found in environment variables")
        print("Please add your Google Maps API key to .env file:")
        print("GOOGLE_MAPS_API_KEY=your_api_key_here")
        return False
    
    print(f"✅ Google Maps API key found: {api_key[:10]}...")
    
    # Test geocoding
    test_address = "București, România"
    print(f"\n🔍 Testing geocoding for: {test_address}")
    
    try:
        geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': test_address,
            'key': api_key
        }
        
        response = requests.get(geocoding_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            result = data['results'][0]
            location = result['geometry']['location']
            
            print(f"✅ Geocoding successful!")
            print(f"   Address: {result['formatted_address']}")
            print(f"   Coordinates: {location['lat']}, {location['lng']}")
            print(f"   Place ID: {result.get('place_id', 'N/A')}")
            
            # Test reverse geocoding
            print(f"\n🔄 Testing reverse geocoding...")
            reverse_params = {
                'latlng': f"{location['lat']},{location['lng']}",
                'key': api_key
            }
            
            reverse_response = requests.get(geocoding_url, params=reverse_params, timeout=10)
            reverse_response.raise_for_status()
            reverse_data = reverse_response.json()
            
            if reverse_data['status'] == 'OK' and reverse_data['results']:
                reverse_result = reverse_data['results'][0]
                print(f"✅ Reverse geocoding successful!")
                print(f"   Address: {reverse_result['formatted_address']}")
            else:
                print(f"❌ Reverse geocoding failed: {reverse_data.get('status', 'Unknown error')}")
            
            return True
        else:
            print(f"❌ Geocoding failed: {data.get('status', 'Unknown error')}")
            if data.get('error_message'):
                print(f"   Error: {data['error_message']}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_content_media_agent():
    """Test the content media agent Google Maps integration"""
    print("\n🤖 Testing Content Media Agent Google Maps Integration")
    print("=" * 50)
    
    # Check if the agent is running
    agent_url = "http://localhost:8002"
    
    try:
        # Test health endpoint
        health_response = requests.get(f"{agent_url}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Content Media Agent is running")
        else:
            print("❌ Content Media Agent is not running")
            print("Start it with: python awesome-mcp-servers/content_media_agent.py")
            return False
    except requests.ConnectionError:
        print("❌ Content Media Agent is not running")
        print("Start it with: python awesome-mcp-servers/content_media_agent.py")
        return False
    
    # Test Google Maps integration tool
    try:
        test_data = {
            "name": "google_maps_integration",
            "arguments": {
                "operation": "geocode",
                "address": "București, România"
            }
        }
        
        response = requests.post(f"{agent_url}/call", json=test_data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        print("✅ Google Maps integration tool called successfully")
        print(f"Result: {json.dumps(result, indent=2)}")
        
        return True
        
    except requests.RequestException as e:
        print(f"❌ Error calling Google Maps integration: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Google Maps Integration Test Suite")
    print("=" * 50)
    
    # Test 1: Direct Google Maps API
    api_test = test_google_maps_api()
    
    # Test 2: Content Media Agent integration
    agent_test = test_content_media_agent()
    
    print("\n📊 Test Results Summary")
    print("=" * 50)
    print(f"Google Maps API Direct Test: {'✅ PASSED' if api_test else '❌ FAILED'}")
    print(f"Content Media Agent Test: {'✅ PASSED' if agent_test else '❌ FAILED'}")
    
    if api_test and agent_test:
        print("\n🎉 All tests passed! Google Maps integration is working correctly.")
    elif api_test:
        print("\n⚠️  Google Maps API works, but agent integration needs attention.")
    else:
        print("\n❌ Google Maps API test failed. Check your API key and configuration.")
    
    print("\n💡 To use Google Maps integration:")
    print("1. Make sure your API key is in .env file")
    print("2. Enable these APIs in Google Cloud Console:")
    print("   - Maps JavaScript API")
    print("   - Geocoding API")
    print("   - Places API")
    print("3. Start the content media agent")
    print("4. Use the google_maps_integration tool")

if __name__ == "__main__":
    main()
