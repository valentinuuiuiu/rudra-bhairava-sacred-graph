"""
MCP Orchestrator - Wrapper for Smart MCP Orchestrator
This file provides backward compatibility and simpler import interface
"""

from .smart_mcp_orchestrator import SmartMCPOrchestrator
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class MCPOrchestrator:
    """
    Main MCP Orchestrator class that wraps the Smart Pydantic-based orchestrator
    Provides a simple interface for the Django views
    """
    
    def __init__(self):
        """Initialize the orchestrator with the smart Pydantic model"""
        try:
            self.smart_orchestrator = SmartMCPOrchestrator()
            logger.info("MCP Orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MCP Orchestrator: {e}")
            raise
    
    async def process_request(self, user_message: str, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Process user request using the smart orchestrator
        
        Args:
            user_message: The user's message/request
            conversation_history: Optional conversation history
            
        Returns:
            Dict containing response, tools_used, and tool_results
        """
        try:
            # Use the smart orchestrator to process the request
            mcp_response = await self.smart_orchestrator.process_request(user_message, conversation_history)
            
            # Convert to the expected format for Django views
            return {
                'response': mcp_response.response,
                'tools_used': mcp_response.tools_used,
                'tool_results': mcp_response.tool_results,
                'intent_analysis': mcp_response.intent_analysis.dict() if mcp_response.intent_analysis else None,
                'reasoning': mcp_response.reasoning
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return {
                'response': f"I apologize, but I encountered an error while processing your request: {str(e)}",
                'tools_used': [],
                'tool_results': [],
                'intent_analysis': None,
                'reasoning': f"Error occurred: {str(e)}"
            }
    
    def get_server_status(self) -> Dict[str, Any]:
        """Get status of all MCP servers"""
        try:
            servers = self.smart_orchestrator.mcp_servers
            status = {}
            
            for server_type, config in servers.items():
                status[server_type.value] = {
                    'name': config.name,
                    'url': config.url,
                    'port': config.port,
                    'description': config.description,
                    'tools': config.tools,
                    'status': 'simulated'  # Until real SSE implementation
                }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting server status: {e}")
            return {}
