
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv

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
