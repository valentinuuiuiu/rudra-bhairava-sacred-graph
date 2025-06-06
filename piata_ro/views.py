from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
import os
from dotenv import load_dotenv

try:
    from praisonai import PraisonAI
except ImportError:
    PraisonAI = None

def home(request):
    """Home page view"""
    return HttpResponse("""
    <html>
    <head>
        <title>🛒 Piața RO - Romanian Marketplace</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .motto { font-style: italic; text-align: center; color: #7f8c8d; margin-bottom: 30px; }
            .links { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
            .link-card { background: #3498db; color: white; padding: 20px; border-radius: 8px; text-decoration: none; text-align: center; transition: background 0.3s; }
            .link-card:hover { background: #2980b9; color: white; text-decoration: none; }
            .api-links { margin-top: 20px; }
            .api-links a { display: inline-block; margin: 5px 10px; padding: 8px 15px; background: #27ae60; color: white; border-radius: 5px; text-decoration: none; }
            .api-links a:hover { background: #219a52; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛒 Piața RO - Romanian Marketplace Platform</h1>
            <p class="motto">Acknowledging The Limitations of The AI is acknowledging The Limitations of Our OLD Patterns Stupid Mind, Dare to Dream and The AI will make it Real</p>
            
            <p>Welcome to the Romanian Marketplace Platform! This is a modern marketplace application built with Django.</p>
            
            <div class="links">
                <a href="/admin/" class="link-card">
                    <h3>📊 Admin Panel</h3>
                    <p>Manage the marketplace</p>
                </a>
                <a href="/api/" class="link-card">
                    <h3>🔧 API Documentation</h3>
                    <p>Explore the REST API</p>
                </a>
            </div>
            
            <div class="api-links">
                <h3>🚀 Available Endpoints:</h3>
                <a href="/api/categories/">Categories</a>
                <a href="/api/listings/">Listings</a>
                <a href="/api/users/">Users</a>
                <a href="/test_endpoint/">Test Endpoint</a>
                <a href="/mcp/process/">MCP Processor</a>
            </div>
            
            <div style="margin-top: 30px; padding: 20px; background: #ecf0f1; border-radius: 8px;">
                <h3>🔧 Getting Started:</h3>
                <p>1. Visit <strong>/admin/</strong> to manage the application</p>
                <p>2. Explore <strong>/api/</strong> to see the REST API endpoints</p>
                <p>3. Check out the marketplace categories and listings</p>
            </div>
        </div>
    </body>
    </html>
    """)

@csrf_exempt
def test_endpoint(request):
    """Simple test endpoint"""
    return JsonResponse({
        "status": "success",
        "message": "Basic Django endpoint working",
        "received_data": request.POST.dict()
    })

@csrf_exempt
def process_mcp_query(request):
    """Process MCP queries with PraisonAI using auto-configured GPT-4o-mini"""
    try:
        if PraisonAI is None:
            return JsonResponse({
                "error": "PraisonAI not available. Please check installation.",
                "status": "error"
            }, status=500)
            
        query = request.POST.get("query", "")
        load_dotenv()
        praison = PraisonAI(
            auto=True,
            framework="django"
        )
        result = praison.process(
            f"Process this MCP query: {query}",
            model=os.getenv('OPENAI_BASE_MODEL'),
            api_key=os.getenv('OPENAI_API_KEY')
        )
        return JsonResponse({
            "result": result,
            "status": "success"
        })
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "status": "error"
        }, status=500)
