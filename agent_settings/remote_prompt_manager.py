import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, List, Union

class RemotePromptManager:
    def __init__(self, mcp_server_url: Optional[str] = None, auth_token: Optional[str] = None):
        self.auth_token = auth_token
        """Initialize with optional MCP server URL"""
        self.mcp_server_url = mcp_server_url
        self.local_storage = os.path.expanduser("~/.agent_settings/prompts")
        os.makedirs(self.local_storage, exist_ok=True)

    async def save_prompt(self, prompt_name: str, prompt_content: Dict, remote: bool = True) -> bool:
        """Save prompt to remote MCP server or local storage"""
        if remote and self.mcp_server_url:
            try:
                response = requests.post(
                    f"{self.mcp_server_url}/prompts",
                    json={"name": prompt_name, "content": prompt_content},
                    headers={"Content-Type": "application/json"}
                )
                return response.status_code == 200
            except Exception as e:
                print(f"Remote save failed, falling back to local: {e}")
        
        # Fallback to local storage
        try:
            local_path = os.path.join(self.local_storage, f"{prompt_name}.json")
            with open(local_path, 'w', encoding='utf-8') as f:
                json.dump(prompt_content, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Local save failed: {e}")
            return False

    async def load_prompt(self, prompt_name: str, remote: bool = True) -> Optional[Dict]:
        """Load prompt from remote or local storage"""
        if remote and self.mcp_server_url:
            try:
                response = requests.get(f"{self.mcp_server_url}/prompts/{prompt_name}")
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Remote load failed, trying local: {e}")
        
        # Fallback to local storage
        local_path = os.path.join(self.local_storage, f"{prompt_name}.json")
        if os.path.exists(local_path):
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Local load failed: {e}")
        return None

    async def list_prompts(self, remote: bool = True) -> List[str]:
        """List available prompts from remote or local storage"""
        if remote and self.mcp_server_url:
            try:
                response = requests.get(f"{self.mcp_server_url}/prompts")
                if response.status_code == 200:
                    return response.json().get("prompts", [])
            except Exception as e:
                print(f"Remote list failed, trying local: {e}")
        
        # Fallback to local storage
        if os.path.exists(self.local_storage):
            return [
                f[:-5] for f in os.listdir(self.local_storage)
                if f.endswith('.json')
            ]
        return []

    async def fetch_web_content(self, url: str) -> str:
        """Fetch web content using MCP fetch tool"""
        try:
            # Use MCP fetch tool to get web content
            fetch_result = await self._use_mcp_tool(
                server_name="fetch",
                tool_name="fetch",
                arguments={"url": url, "max_length": 5000}
            )
            return fetch_result.get("content", "")
        except Exception as e:
            print(f"Failed to fetch web content: {e}")
            return ""

    async def _use_mcp_tool(self, server_name: str, tool_name: str, arguments: Dict) -> Dict:
        """Helper method to interact with MCP tools with authentication support"""
        if not self.mcp_server_url:
            raise ValueError("MCP server URL not configured")
            
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
            
        try:
            response = requests.post(
                f"{self.mcp_server_url}/tools/{server_name}/{tool_name}",
                json=arguments,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"MCP tool error: {e}")
            return {"status": "error", "message": str(e)}

    async def test_connection(self) -> bool:
        """Test connection to MCP server"""
        if not self.mcp_server_url:
            return False
            
        try:
            response = requests.get(
                f"{self.mcp_server_url}/health",
                headers={"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
            )
            return response.status_code == 200
        except Exception:
            return False

    async def list_available_tools(self) -> Dict[str, List[str]]:
        """List available tools from MCP server"""
        if not self.mcp_server_url:
            return {}
            
        try:
            response = requests.get(
                f"{self.mcp_server_url}/tools",
                headers={"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"Failed to list tools: {e}")
            return {}

# Example usage with Puppeteer integration
async def example_usage():
    manager = RemotePromptManager(mcp_server_url="https://api.mcp-server.example.com")
    
    # Save prompt to remote server
    await manager.save_prompt(
        "web_scraping_prompt",
        {
            "name": "Web Scraping Example",
            "instructions": "Scrape product data from e-commerce site",
            "target_url": "https://example.com/products"
        }
    )
    
    # Fetch web content using MCP tools
    content = await manager.fetch_web_content("https://example.com")
    print(f"Fetched content length: {len(content)}")
    
    # Load prompt
    prompt = await manager.load_prompt("web_scraping_prompt")
    print(f"Loaded prompt: {prompt}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())