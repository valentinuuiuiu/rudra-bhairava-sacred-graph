from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
import asyncio
import httpx
from datetime import datetime

from .models_chat import ChatConversation, ChatMessage

class PiataAIAssistantAdmin(admin.ModelAdmin):
    """Custom admin for AI Assistant interface"""
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ai-assistant/', self.admin_site.admin_view(self.ai_assistant_view), name='ai_assistant'),
            path('ai-assistant/chat/', self.admin_site.admin_view(self.chat_api), name='ai_assistant_chat'),
        ]
        return custom_urls + urls
    
    def ai_assistant_view(self, request):
        """Main AI Assistant interface"""
        conversations = ChatConversation.objects.filter(user=request.user)[:10]
        context = {
            'title': 'Piața.ro AI Assistant',
            'conversations': conversations,
            'mcp_status': self.get_mcp_status(),
        }
        return render(request, 'admin/ai_assistant.html', context)
    
    @csrf_exempt
    def chat_api(self, request):
        """API endpoint for chat functionality"""
        if request.method == 'POST':
            data = json.loads(request.body)
            message = data.get('message', '')
            conversation_id = data.get('conversation_id')
            
            # Get or create conversation
            if conversation_id:
                conversation = ChatConversation.objects.get(id=conversation_id, user=request.user)
            else:
                conversation = ChatConversation.objects.create(
                    user=request.user,
                    title=message[:50] + "..." if len(message) > 50 else message
                )
            
            # Save user message
            user_message = ChatMessage.objects.create(
                conversation=conversation,
                message=message,
                is_user=True
            )
            
            # Process with AI Assistant
            response = asyncio.run(self.process_with_assistant(message))
            
            # Save assistant response
            assistant_message = ChatMessage.objects.create(
                conversation=conversation,
                message=message,
                response=response['response'],
                is_user=False,
                agent_used=response.get('agent_used', 'master')
            )
            
            return JsonResponse({
                'response': response['response'],
                'conversation_id': conversation.id,
                'agent_used': response.get('agent_used', 'master'),
                'timestamp': datetime.now().isoformat()
            })
        
        return JsonResponse({'error': 'Invalid request'})
    
    async def process_with_assistant(self, message):
        """Process message through MCP agents"""
        # Determine which agent to use based on message content
        agent_url = self.route_to_agent(message)
        
        try:
            async with httpx.AsyncClient() as client:
                # This is a simplified call - you'd need to implement proper MCP protocol
                response = await client.post(
                    agent_url,
                    json={
                        'method': 'tools/call',
                        'params': {
                            'name': 'process_request',
                            'arguments': {'message': message}
                        }
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        'response': result.get('content', 'I processed your request.'),
                        'agent_used': self.get_agent_name(agent_url)
                    }
                else:
                    return {
                        'response': f"I understand you want help with: {message}. Let me process this for you.",
                        'agent_used': 'fallback'
                    }
        except Exception as e:
            return {
                'response': f"I'm here to help! You asked about: {message}. How can I assist you further?",
                'agent_used': 'error_handler'
            }
    
    def route_to_agent(self, message):
        """Route message to appropriate MCP agent"""
        message_lower = message.lower()
        
        # Database operations
        if any(word in message_lower for word in ['listing', 'user', 'search', 'data', 'database', 'create', 'update', 'delete']):
            return 'http://localhost:8002/sse'
        
        # Financial operations  
        elif any(word in message_lower for word in ['payment', 'invoice', 'money', 'revenue', 'financial', 'accounting', 'profit']):
            return 'http://localhost:8003/sse'
        
        # Marketing operations
        elif any(word in message_lower for word in ['marketing', 'advertising', 'seo', 'social', 'promote', 'campaign']):
            return 'http://localhost:8001/sse'
        
        # Default to database agent
        return 'http://localhost:8002/sse'
    
    def get_agent_name(self, url):
        """Get agent name from URL"""
        if '8001' in url:
            return 'Marketing Agent'
        elif '8002' in url:
            return 'Database Agent'
        elif '8003' in url:
            return 'Accounting Agent'
        return 'Master Agent'
    
    def get_mcp_status(self):
        """Check MCP agents status"""
        agents = {
            'Database Agent (8002)': 'http://localhost:8002',
            'Accounting Agent (8003)': 'http://localhost:8003', 
            'Marketing Agent (8001)': 'http://localhost:8001'
        }
        
        status = {}
        for name, url in agents.items():
            try:
                import requests
                response = requests.get(url, timeout=2)
                status[name] = 'Online' if response.status_code == 200 else 'Offline'
            except:
                status[name] = 'Offline'
        
        return status

# Register the AI Assistant in admin
admin.site.register_view('ai-assistant/', view=PiataAIAssistantAdmin().ai_assistant_view, name='AI Assistant')
