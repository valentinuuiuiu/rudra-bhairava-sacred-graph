#!/usr/bin/env python3
"""
Test script for PraisonAI Django integration
Tests the MCP endpoints and PraisonAI functionality
"""

import requests
import json
import sys

def test_endpoint(url, data=None, method='GET'):
    """Test an endpoint and return the response"""
    try:
        if method == 'POST':
            response = requests.post(url, data=data, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        
        print(f"\n{'='*60}")
        print(f"Testing {method} {url}")
        print(f"Status Code: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            return result
        else:
            print(f"Response (text): {response.text[:500]}...")
            return response.text
            
    except Exception as e:
        print(f"Error testing {url}: {str(e)}")
        return None

def main():
    """Main test function"""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 Testing Piața RO Django + PraisonAI Integration")
    print("="*60)
    
    # Test 1: Home page
    test_endpoint(f"{base_url}/")
    
    # Test 2: Basic test endpoint
    test_endpoint(f"{base_url}/test_endpoint/")
    
    # Test 3: MCP Processor GET (should show status)
    test_endpoint(f"{base_url}/mcp/process/")
    
    # Test 4: MCP Agents GET (should show available agents)
    test_endpoint(f"{base_url}/mcp/agents/")
    
    # Test 5: API Categories
    test_endpoint(f"{base_url}/api/categories/")
    
    # Test 6: API Listings
    test_endpoint(f"{base_url}/api/listings/")
    
    # Test 7: MCP Processor with query
    print("\n" + "="*60)
    print("Testing PraisonAI Query Processing...")
    
    test_queries = [
        "What categories are available in the marketplace?",
        "Show me cheap apartments in Bucharest",
        "List all electronics for sale",
        "Help me optimize my listing for better visibility"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        result = test_endpoint(
            f"{base_url}/mcp/process/", 
            data={'query': query}, 
            method='POST'
        )
        
        if result and 'error' not in result:
            print("✅ Query processed successfully")
        else:
            print("❌ Query failed")
    
    print("\n" + "="*60)
    print("🎉 Test completed! Check the results above.")
    print("If PraisonAI is working, you should see intelligent responses to the queries.")

if __name__ == "__main__":
    main()
