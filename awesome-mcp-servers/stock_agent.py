"""
Stock Agent for Piata.ro Project
An agent that uses the MCP server to interact with marketplace data and provide intelligent responses.
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PiataRoAgent:
    """Agent for interacting with Piata.ro marketplace through MCP server"""
    
    def __init__(self, mcp_server_url: str = "http://localhost:8080"):
        """
        Initialize the agent with MCP server connection details.
        
        Args:
            mcp_server_url: URL of the MCP server
        """
        self.mcp_server_url = mcp_server_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def call_mcp_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Call an MCP tool with the given parameters.
        
        Args:
            tool_name: Name of the MCP tool to call
            **kwargs: Parameters to pass to the tool
        
        Returns:
            Tool response data
        """
        try:
            payload = {
                "tool": tool_name,
                "parameters": kwargs
            }
            
            response = await self.client.post(
                f"{self.mcp_server_url}/tools/{tool_name}",
                json=payload
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    async def get_marketplace_overview(self) -> str:
        """
        Get a comprehensive overview of the marketplace.
        
        Returns:
            Formatted string with marketplace overview
        """
        try:
            # Get statistics
            stats_response = await self.call_mcp_tool("get_listing_stats")
            
            # Get categories
            categories_response = await self.call_mcp_tool("get_categories")
            
            # Get recent listings
            listings_response = await self.call_mcp_tool("get_listings", limit=5)
            
            overview = "# Piata.ro Marketplace Overview\n\n"
            
            # Add statistics
            if "error" not in stats_response:
                stats = stats_response
                overview += "## Statistics\n"
                overview += f"- Total Listings: {stats.get('total_listings', 0)}\n"
                overview += f"- Categories: {stats.get('total_categories', 0)}\n"
                overview += f"- Price Range: ${stats.get('min_price', 0)} - ${stats.get('max_price', 0)}\n"
                overview += f"- Average Price: ${stats.get('avg_price', 0)}\n"
                overview += f"- Featured Listings: {stats.get('featured_listings', 0)}\n\n"
            
            # Add categories
            if "error" not in categories_response:
                categories = categories_response
                if isinstance(categories_response, dict) and "categories" in categories_response:
                    categories = categories_response["categories"]
                if isinstance(categories, list):
                    overview += "## Available Categories\n"
                    for category in categories[:10]:  # Show first 10 categories
                        overview += f"- {category}\n"
                    overview += "\n"
            
            # Add recent listings
            if "error" not in listings_response and isinstance(listings_response, list):
                overview += "## Recent Listings\n"
                for listing in listings_response:
                    if isinstance(listing, dict):
                        overview += f"### {listing.get('title', 'Untitled')}\n"
                        overview += f"**Price:** ${listing.get('price', 0)}\n"
                        overview += f"**Category:** {listing.get('category', 'N/A')}\n"
                        overview += f"**Location:** {listing.get('location', 'N/A')}\n"
                        if listing.get('is_featured'):
                            overview += "**Featured** ⭐\n"
                        overview += "\n"
            
            return overview
            
        except Exception as e:
            return f"Error generating marketplace overview: {str(e)}"
    
    async def search_and_analyze(self, query: str, category: Optional[str] = None, max_price: Optional[float] = None) -> str:
        """
        Search listings and provide analysis.
        
        Args:
            query: Search query
            category: Optional category filter
            max_price: Optional maximum price filter
        
        Returns:
            Formatted analysis of search results
        """
        try:
            # Perform search
            search_params = {"query": query}
            if category:
                search_params["category"] = category
            if max_price:
                search_params["max_price"] = str(max_price)
            
            search_response = await self.call_mcp_tool("search_listings", **search_params)
            
            if "error" in search_response:
                return f"Search error: {search_response['error']}"
            
            if not isinstance(search_response, list) or len(search_response) == 0:
                return f"No listings found for query: '{query}'"
            
            # Analyze results
            analysis = f"# Search Results for '{query}'\n\n"
            analysis += f"Found {len(search_response)} listings\n\n"
            
            # Price analysis
            prices = []
            for listing in search_response:
                if isinstance(listing, dict) and listing.get('price'):
                    prices.append(listing.get('price', 0))
                    
            if prices:
                avg_price = sum(prices) / len(prices)
                min_price = min(prices)
                max_price = max(prices)
                
                analysis += "## Price Analysis\n"
                analysis += f"- Average Price: ${avg_price:.2f}\n"
                analysis += f"- Price Range: ${min_price} - ${max_price}\n\n"
            
            # Category breakdown
            categories = {}
            for listing in search_response:
                if isinstance(listing, dict):
                    cat = listing.get('category', 'Unknown')
                    categories[cat] = categories.get(cat, 0) + 1
            
            if categories:
                analysis += "## Category Breakdown\n"
                for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                    analysis += f"- {cat}: {count} listings\n"
                analysis += "\n"
            
            # Show top results
            analysis += "## Top Results\n"
            max_results = min(5, len(search_response))
            for i in range(max_results):
                listing = search_response[i]
                if isinstance(listing, dict):
                    analysis += f"### {i+1}. {listing.get('title', 'Untitled')}\n"
                    analysis += f"**Price:** ${listing.get('price', 0)}\n"
                    analysis += f"**Category:** {listing.get('category', 'N/A')}\n"
                    analysis += f"**Location:** {listing.get('location', 'N/A')}\n"
                    if listing.get('is_featured'):
                        analysis += "**Featured** ⭐\n"
                    
                    description = listing.get('description', '')
                    if len(description) > 100:
                        description = description[:100] + "..."
                    analysis += f"**Description:** {description}\n\n"
            
            return analysis
            
        except Exception as e:
            return f"Error performing search and analysis: {str(e)}"
    
    async def add_listing_with_validation(self, title: str, description: str, price: float, 
                                        category: str, location: str, contact_info: str) -> str:
        """
        Add a new listing with validation and feedback.
        
        Args:
            title: Listing title
            description: Listing description
            price: Listing price
            category: Listing category
            location: Listing location
            contact_info: Contact information
        
        Returns:
            Success message or error details
        """
        try:
            # Validate inputs
            if not title or len(title.strip()) < 3:
                return "Error: Title must be at least 3 characters long"
            
            if not description or len(description.strip()) < 10:
                return "Error: Description must be at least 10 characters long"
            
            if price <= 0:
                return "Error: Price must be greater than 0"
            
            if not category or not category.strip():
                return "Error: Category is required"
            
            if not location or not location.strip():
                return "Error: Location is required"
            
            if not contact_info or not contact_info.strip():
                return "Error: Contact information is required"
            
            # Add the listing
            response = await self.call_mcp_tool(
                "add_listing",
                title=title.strip(),
                description=description.strip(),
                price=price,
                category=category.strip(),
                location=location.strip(),
                contact_info=contact_info.strip()
            )
            
            if "error" in response:
                return f"Failed to add listing: {response['error']}"
            
            if response.get("success"):
                return f"✅ Listing added successfully! ID: {response.get('listing_id')}"
            
            return "Listing submission completed, but status unclear"
            
        except Exception as e:
            return f"Error adding listing: {str(e)}"
    
    async def get_category_insights(self, category: str) -> str:
        """
        Get insights about a specific category.
        
        Args:
            category: Category to analyze
        
        Returns:
            Formatted insights about the category
        """
        try:
            # Get listings for this category
            category_listings = await self.call_mcp_tool("get_listings", limit=50, category=category)
            
            if "error" in category_listings:
                return f"Error getting category data: {category_listings['error']}"
            
            if not isinstance(category_listings, list) or len(category_listings) == 0:
                return f"No listings found in category: {category}"
            
            insights = f"# Category Insights: {category}\n\n"
            insights += f"Total listings in category: {len(category_listings)}\n\n"
            
            # Price analysis
            prices = [listing.get('price', 0) for listing in category_listings if listing.get('price')]
            if prices:
                avg_price = sum(prices) / len(prices)
                min_price = min(prices)
                max_price = max(prices)
                
                insights += "## Price Analysis\n"
                insights += f"- Average Price: ${avg_price:.2f}\n"
                insights += f"- Lowest Price: ${min_price}\n"
                insights += f"- Highest Price: ${max_price}\n\n"
            
            # Location analysis
            locations = {}
            for listing in category_listings:
                loc = listing.get('location', 'Unknown')
                locations[loc] = locations.get(loc, 0) + 1
            
            if locations:
                insights += "## Top Locations\n"
                for loc, count in sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5]:
                    insights += f"- {loc}: {count} listings\n"
                insights += "\n"
            
            # Featured listings
            featured = [listing for listing in category_listings if listing.get('is_featured')]
            if featured:
                insights += f"## Featured Listings ({len(featured)})\n"
                for listing in featured[:3]:
                    insights += f"- **{listing.get('title', 'Untitled')}** - ${listing.get('price', 0)}\n"
                insights += "\n"
            
            return insights
            
        except Exception as e:
            return f"Error generating category insights: {str(e)}"

# Example usage and testing functions
async def test_agent():
    """Test the agent functionality"""
    async with PiataRoAgent() as agent:
        print("=== Marketplace Overview ===")
        overview = await agent.get_marketplace_overview()
        print(overview)
        
        print("\n=== Search Test ===")
        search_results = await agent.search_and_analyze("laptop", max_price=1000)
        print(search_results)
        
        print("\n=== Category Insights Test ===")
        insights = await agent.get_category_insights("Electronics")
        print(insights)

if __name__ == "__main__":
    # Run tests
    asyncio.run(test_agent())
