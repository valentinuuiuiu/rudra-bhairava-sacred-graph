

import httpx
from reflex.config import get_config

config = get_config()
DJANGO_API_URL = "http://localhost:8000/api"  # Update if Django runs on different port

async def fetch_listings():
    """Fetch listings from Django API"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_API_URL}/listings/")
        return response.json()

async def post_mcp_query(query: str):
    """Send MCP queries to Django backend"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DJANGO_API_URL}/mcp/process/",
            json={"query": query}
        )
        return response.json()

