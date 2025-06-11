"""
Stock Agent for Piata.ro Project
An MCP server that provides real database operations for marketplace stock and analytics.
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'piata_ro.settings')

import django
from django.conf import settings
django.setup()

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, Avg, Sum, Q, Min, Max
from django.db import transaction
from django.contrib.auth import authenticate
from asgiref.sync import sync_to_async
from fastapi import FastAPI, HTTPException
import uvicorn
from fastmcp import FastMCP

# Import marketplace models
from marketplace.models import Listing, Category

# Initialize FastMCP server for stock operations
mcp = FastMCP("Piața.ro Stock Agent - Real Database Operations")

# Helper functions to make Django ORM calls async-safe
def _get_marketplace_overview_sync():
    """Synchronous version of marketplace overview for async wrapping"""
    try:
        # Total listings
        total_listings = Listing.objects.count()
        active_listings = Listing.objects.filter(status='active').count()
        sold_listings = Listing.objects.filter(status='sold').count()
        pending_listings = Listing.objects.filter(status='pending').count()
        
        # Category statistics
        categories_with_counts = Category.objects.annotate(
            listing_count=Count('listings')
        ).order_by('-listing_count')[:10]
        
        # Price statistics
        price_stats = Listing.objects.filter(
            status='active', 
            price__isnull=False
        ).aggregate(
            avg_price=Avg('price'),
            min_price=Min('price'),
            max_price=Max('price')
        )
        
        # Recent activity (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_listings = Listing.objects.filter(
            created_at__gte=week_ago
        ).count()
        
        # Location statistics
        location_stats = Listing.objects.filter(
            status='active'
        ).values('location').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        return {
            "success": True,
            "overview": {
                "total_listings": total_listings,
                "active_listings": active_listings,
                "sold_listings": sold_listings,
                "pending_listings": pending_listings,
                "recent_listings_week": recent_listings,
                "top_categories": [
                    {
                        "name": cat.name,
                        "count": cat.listing_count,
                        "slug": cat.slug
                    }
                    for cat in categories_with_counts
                ],
                "price_statistics": {
                    "average_price": float(price_stats['avg_price'] or 0),
                    "min_price": float(price_stats['min_price'] or 0),
                    "max_price": float(price_stats['max_price'] or 0)
                },
                "top_locations": [
                    {
                        "location": loc['location'],
                        "count": loc['count']
                    }
                    for loc in location_stats
                ]
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get marketplace overview: {str(e)}",
            "overview": {}
        }

def _get_category_analytics_sync(category_name: str):
    """Synchronous version of category analytics"""
    try:
        # Find category by name or slug
        try:
            category = Category.objects.get(
                Q(name__icontains=category_name) | Q(slug=category_name)
            )
        except Category.DoesNotExist:
            return {
                "success": False,
                "error": f"Category '{category_name}' not found",
                "analytics": {}
            }
        
        # Get listings for this category
        listings = Listing.objects.filter(category=category)
        active_listings = listings.filter(status='active')
        
        return {
            "success": True,
            "category": category.name,
            "analytics": {
                "total_listings": listings.count(),
                "active_listings": active_listings.count(),
                "sample_listings": [
                    {
                        "id": listing.id,
                        "title": listing.title,
                        "price": float(listing.price) if listing.price else None,
                        "location": listing.location
                    }
                    for listing in active_listings[:5]
                ]
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get category analytics: {str(e)}",
            "analytics": {}
        }

def _get_product_stock_info_sync(listing_id: str):
    """Synchronous version of product stock info"""
    try:
        listing = Listing.objects.select_related('category', 'user').get(id=listing_id)
        
        return {
            "success": True,
            "listing": {
                "id": listing.id,
                "title": listing.title,
                "description": listing.description,
                "price": float(listing.price) if listing.price else None,
                "category": listing.category.name if listing.category else None,
                "location": listing.location,
                "status": listing.status,
                "seller": {
                    "username": listing.user.username,
                    "id": listing.user.id
                },
                "created_at": listing.created_at.isoformat()
            }
        }
        
    except Listing.DoesNotExist:
        return {
            "success": False,
            "error": f"Listing with ID {listing_id} not found"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get listing info: {str(e)}"
        }

def _search_listings_sync(**kwargs):
    """Synchronous version of search listings"""
    try:
        query = kwargs.get('query')
        category = kwargs.get('category') 
        location = kwargs.get('location')
        status = kwargs.get('status', 'active')
        limit = kwargs.get('limit', 20)
        
        listings = Listing.objects.select_related('category', 'user')
        
        # Apply filters
        if status:
            listings = listings.filter(status=status)
            
        if query:
            listings = listings.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            
        if category:
            try:
                cat = Category.objects.get(
                    Q(name__icontains=category) | Q(slug=category)
                )
                listings = listings.filter(category=cat)
            except Category.DoesNotExist:
                pass
                
        if location:
            listings = listings.filter(location__icontains=location)
        
        # Order by relevance (newest first)
        listings = listings.order_by('-created_at')[:limit]
        
        results = []
        for listing in listings:
            results.append({
                "id": listing.id,
                "title": listing.title,
                "price": float(listing.price) if listing.price else None,
                "category": listing.category.name if listing.category else None,
                "location": listing.location,
                "status": listing.status,
                "created_at": listing.created_at.isoformat(),
                "seller_username": listing.user.username
            })
        
        return {
            "success": True,
            "total_results": len(results),
            "results": results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Search failed: {str(e)}",
            "results": []
        }

def _get_user_listings_sync(username: str):
    """Synchronous version of get user listings"""
    try:
        user = User.objects.get(username=username)
        listings = Listing.objects.filter(user=user).select_related('category').order_by('-created_at')
        
        results = []
        for listing in listings:
            results.append({
                "id": listing.id,
                "title": listing.title,
                "price": float(listing.price) if listing.price else None,
                "category": listing.category.name if listing.category else None,
                "location": listing.location,
                "status": listing.status,
                "created_at": listing.created_at.isoformat()
            })
        
        return {
            "success": True,
            "user": {
                "username": user.username,
                "id": user.id
            },
            "total_listings": len(results),
            "listings": results
        }
        
    except User.DoesNotExist:
        return {
            "success": False,
            "error": f"User '{username}' not found"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get user listings: {str(e)}"
        }

def _create_user_sync(username: str, email: str, password: str, first_name: str = "", last_name: str = ""):
    """Synchronous version of create user"""
    try:
        with transaction.atomic():
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return {
                    "success": False,
                    "error": f"User with username '{username}' already exists",
                    "user_id": None
                }
            
            if User.objects.filter(email=email).exists():
                return {
                    "success": False,
                    "error": f"User with email '{email}' already exists",
                    "user_id": None
                }
            
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            return {
                "success": True,
                "message": f"User '{username}' created successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "date_joined": user.date_joined.isoformat()
                }
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create user: {str(e)}",
            "user_id": None
        }

def _authenticate_user_sync(username: str, password: str):
    """Synchronous version of authenticate user"""
    try:
        user = authenticate(username=username, password=password)
        
        if user is not None:
            return {
                "success": True,
                "authenticated": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "last_login": user.last_login.isoformat() if user.last_login else None,
                    "is_active": user.is_active
                }
            }
        else:
            return {
                "success": True,
                "authenticated": False,
                "message": "Invalid username or password"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Authentication failed: {str(e)}"
        }

def _create_listing_sync(title: str, description: str, price: float, category_name: str, 
                        location: str, username: str):
    """Synchronous version of create listing"""
    try:
        with transaction.atomic():
            # Get user
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return {
                    "success": False,
                    "error": f"User '{username}' not found"
                }
            
            # Get or create category
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': category_name.lower().replace(' ', '-')}
            )
            
            # Create listing
            listing = Listing.objects.create(
                title=title,
                description=description,
                price=price,
                category=category,
                location=location,
                user=user,
                status='active'
            )
            
            return {
                "success": True,
                "message": f"Listing '{title}' created successfully",
                "listing": {
                    "id": listing.id,
                    "title": listing.title,
                    "price": float(listing.price) if listing.price else None,
                    "category": listing.category.name,
                    "location": listing.location,
                    "status": listing.status,
                    "created_at": listing.created_at.isoformat()
                }
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create listing: {str(e)}"
        }

def _execute_custom_query_sync(query: str):
    """Synchronous version of execute custom query (SELECT only)"""
    try:
        # Security check - only allow SELECT statements
        query_upper = query.strip().upper()
        if not query_upper.startswith('SELECT'):
            return {
                "success": False,
                "error": "Only SELECT queries are allowed for security reasons"
            }
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                
                return {
                    "success": True,
                    "query": query,
                    "columns": columns,
                    "results": results,
                    "row_count": len(results)
                }
            else:
                return {
                    "success": True,
                    "query": query,
                    "message": "Query executed successfully (no results returned)"
                }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Query execution failed: {str(e)}"
        }

# Convert sync functions to async using sync_to_async
get_marketplace_overview_async = sync_to_async(_get_marketplace_overview_sync)
get_category_analytics_async = sync_to_async(_get_category_analytics_sync)
get_product_stock_info_async = sync_to_async(_get_product_stock_info_sync)
search_listings_async = sync_to_async(_search_listings_sync)
get_user_listings_async = sync_to_async(_get_user_listings_sync)
create_user_async = sync_to_async(_create_user_sync)
authenticate_user_async = sync_to_async(_authenticate_user_sync)
create_listing_async = sync_to_async(_create_listing_sync)
execute_custom_query_async = sync_to_async(_execute_custom_query_sync)

# Additional MCP Tools for SQL operations
@mcp.tool()
async def create_user(username: str, email: str, password: str, first_name: str = "", last_name: str = "") -> Dict[str, Any]:
    """
    Create a new user in the Django database.
    
    Args:
        username: Unique username for the user
        email: User's email address  
        password: User's password
        first_name: User's first name (optional)
        last_name: User's last name (optional)
        
    Returns:
        Dictionary with user creation status and user info
    """
    return await create_user_async(username, email, password, first_name, last_name)

@mcp.tool()
async def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """
    Authenticate a user with username and password.
    
    Args:
        username: Username to authenticate
        password: Password to verify
        
    Returns:
        Dictionary with authentication result and user info if successful
    """
    return await authenticate_user_async(username, password)

@mcp.tool()
async def create_listing(title: str, description: str, price: float, category_name: str, 
                        location: str, username: str) -> Dict[str, Any]:
    """
    Create a new marketplace listing.
    
    Args:
        title: Listing title
        description: Listing description
        price: Listing price
        category_name: Category name (will be created if doesn't exist)
        location: Listing location
        username: Username of the listing creator
        
    Returns:
        Dictionary with listing creation status and listing info
    """
    return await create_listing_async(title, description, price, category_name, location, username)

@mcp.tool()
async def execute_custom_query(query: str) -> Dict[str, Any]:
    """
    Execute a custom SQL query (SELECT only for security).
    
    Args:
        query: SQL SELECT query to execute
        
    Returns:
        Dictionary with query results
    """
    return await execute_custom_query_async(query)

# Create FastAPI app for REST endpoints
rest_app = FastAPI(title="Piața.ro Database Agent API", version="1.0.0")

# REST API endpoints for tool calls
@rest_app.post("/call")
async def call_tool(request: dict):
    """REST endpoint to call MCP tools"""
    try:
        method = request.get("method")
        params = request.get("params", {})
        
        if method != "tools/call":
            raise HTTPException(status_code=400, detail="Only tools/call method supported")
        
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        # Get the tool from MCP server and call it properly
        available_tools = await mcp.get_tools()
        
        if tool_name not in available_tools:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
        
        # Call the tool function directly (since they're decorated functions)
        tool_function = available_tools[tool_name].fn
        if tool_args:
            result = await tool_function(**tool_args)
        else:
            result = await tool_function()
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": result
        }
        
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -1,
                "message": str(e)
            }
        }

@rest_app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    try:
        tools = await mcp.get_tools()
        return {
            "tools": [
                {
                    "name": name,
                    "description": tool.description or "No description available"
                }
                for name, tool in tools.items()
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tools: {str(e)}")

@rest_app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "piata-database-agent"}

# Main execution block
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Piata.ro Stock MCP Agent")
    parser.add_argument("--port", type=int, default=8003, help="Port to run the MCP server on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the MCP server to")
    args = parser.parse_args()

    print(f"🚀 Starting Piața.ro Database Agent (Stock + SQL Operations) on {args.host}:{args.port}")
    print("Available tools (connected to real database):")
    print("📊 Stock & Analytics:")
    print("  - get_marketplace_overview: Get comprehensive marketplace statistics")
    print("  - get_category_analytics: Get detailed category analytics")
    print("  - get_product_stock_info: Get specific listing information")
    print("  - search_listings: Search listings with filters")
    print("  - get_user_listings: Get all listings for a user")
    print("👥 User Management:")
    print("  - create_user: Create new users")
    print("  - authenticate_user: Authenticate users")
    print("📝 Listing Management:")
    print("  - create_listing: Create new marketplace listings")
    print("🔍 Custom Queries:")
    print("  - execute_custom_query: Execute custom SELECT queries")
    print(f"\n🎯 Database Agent ready for comprehensive Piata.ro operations on {args.host}:{args.port}!")
    print(f"📡 REST API available at http://{args.host}:{args.port}/call")
    print(f"🔍 Tools list available at http://{args.host}:{args.port}/tools")
    
    # Run the REST API server using uvicorn
    uvicorn.run(rest_app, host=args.host, port=args.port)
