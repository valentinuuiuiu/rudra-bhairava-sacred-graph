#!/usr/bin/env python3
"""
MCP Integration Starter for Piata.ro
This script helps start the MCP agents and test the PraisonAI integration
"""

import os
import sys
import subprocess
import time
import requests
import json
from pathlib import Path

def check_django_server():
    """Check if Django server is running"""
    try:
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_mcp_agent(port, name):
    """Check if MCP agent is running on given port"""
    try:
        response = requests.get(f'http://localhost:{port}/', timeout=5)
        return True
    except:
        return False

def start_mcp_agent(script_path, port, name):
    """Start an MCP agent"""
    print(f"🚀 Starting {name} on port {port}...")
    try:
        process = subprocess.Popen(
            [sys.executable, script_path],
            cwd=Path(__file__).parent / 'awesome-mcp-servers',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # Give it time to start
        
        if check_mcp_agent(port, name):
            print(f"✅ {name} started successfully on port {port}")
            return process
        else:
            print(f"❌ {name} failed to start on port {port}")
            return None
    except Exception as e:
        print(f"❌ Error starting {name}: {e}")
        return None

def test_integration():
    """Test the PraisonAI integration"""
    print("\n🧪 Testing PraisonAI Integration...")
    
    # Test basic MCP processor
    try:
        response = requests.get('http://127.0.0.1:8000/mcp/process/')
        if response.status_code == 200:
            print("✅ MCP Processor endpoint is working")
        else:
            print(f"❌ MCP Processor endpoint error: {response.status_code}")
    except Exception as e:
        print(f"❌ MCP Processor endpoint error: {e}")
    
    # Test MCP agents endpoint
    try:
        response = requests.get('http://127.0.0.1:8000/mcp/agents/')
        if response.status_code == 200:
            print("✅ MCP Agents endpoint is working")
        else:
            print(f"❌ MCP Agents endpoint error: {response.status_code}")
    except Exception as e:
        print(f"❌ MCP Agents endpoint error: {e}")
    
    # Test sample query
    print("\n🔍 Testing sample queries...")
    
    queries = [
        "Show me all categories",
        "Find cheap apartments in Bucharest", 
        "What electronics are available?"
    ]
    
    for query in queries:
        print(f"\nTesting query: '{query}'")
        try:
            response = requests.post(
                'http://127.0.0.1:8000/mcp/process/',
                data={'query': query},
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Query processed: {result.get('status', 'unknown')}")
                if 'data' in result and result['data']:
                    print(f"   Found {len(result['data'])} results")
            else:
                print(f"❌ Query failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Query error: {e}")

def main():
    print("🛒 Piata.ro - MCP Integration Starter")
    print("=" * 40)
    
    # Check if Django is running
    if not check_django_server():
        print("❌ Django server is not running!")
        print("Please start Django server first: python manage.py runserver")
        return
    
    print("✅ Django server is running")
    
    # MCP Agents to start
    agents = [
        {
            'script': 'django_sql_agent.py',
            'port': 8002,
            'name': 'Django SQL Agent'
        },
        {
            'script': 'advertising_agent.py', 
            'port': 8001,
            'name': 'Advertising Agent'
        },
        {
            'script': 'stock_agent.py',
            'port': 8003,
            'name': 'Stock Agent'
        }
    ]
    
    # Start MCP agents
    processes = []
    for agent in agents:
        if not check_mcp_agent(agent['port'], agent['name']):
            process = start_mcp_agent(agent['script'], agent['port'], agent['name'])
            if process:
                processes.append(process)
        else:
            print(f"✅ {agent['name']} is already running on port {agent['port']}")
    
    # Test integration
    test_integration()
    
    print("\n🎉 Integration setup complete!")
    print("\n📋 Available endpoints:")
    print("   • http://127.0.0.1:8000/mcp/process/ - PraisonAI processor")
    print("   • http://127.0.0.1:8000/mcp/agents/ - Direct MCP agent interaction")
    print("   • http://127.0.0.1:8000/api/listings/ - Django REST API")
    print("   • http://127.0.0.1:8000/api/categories/ - Categories API")
    
    print("\n💡 Example queries to try:")
    print("   • 'Show me cheap apartments in Bucharest'")
    print("   • 'What electronics are available?'")
    print("   • 'List all categories'")
    print("   • 'Find featured listings'")
    
    if processes:
        print("\n⏹️  Press Ctrl+C to stop all MCP agents")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping MCP agents...")
            for process in processes:
                process.terminate()
            print("✅ All agents stopped")

if __name__ == "__main__":
    main()
