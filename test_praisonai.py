#!/usr/bin/env python3
"""
Simple test script to verify PraisonAI integration
"""

import requests
import json
import sys

def test_mcp_endpoint():
    """Test the MCP endpoint"""
    
    # Test GET request (should show ready status)
    print("🔍 Testing GET request...")
    try:
        response = requests.get("http://127.0.0.1:8000/mcp/process/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"❌ GET request failed: {e}")
        return False
    
    # Test POST request with query
    print("🔍 Testing POST request with query...")
    try:
        test_data = {
            "query": "Analyze the Romanian marketplace trends and suggest 3 popular product categories"
        }
        
        response = requests.post(
            "http://127.0.0.1:8000/mcp/process/",
            data=test_data
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            print("✅ PraisonAI is working correctly!")
            return True
        else:
            print("❌ PraisonAI returned an error")
            return False
            
    except Exception as e:
        print(f"❌ POST request failed: {e}")
        return False

def test_basic_endpoint():
    """Test basic Django endpoint"""
    print("🔍 Testing basic Django endpoint...")
    try:
        response = requests.get("http://127.0.0.1:8000/test_endpoint/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Basic endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing PraisonAI Integration\n")
    
    # Test basic Django functionality first
    if not test_basic_endpoint():
        print("❌ Basic Django functionality is not working!")
        sys.exit(1)
    
    # Test MCP/PraisonAI functionality
    if test_mcp_endpoint():
        print("\n🎉 All tests passed! PraisonAI integration is working correctly.")
    else:
        print("\n❌ PraisonAI integration needs attention.")
        sys.exit(1)
