"""
Content & Media Processing Agent - MCP Server for Piața.ro
A Model Context Protocol server that provides specialized tools for content processing,
image handling, location services, and media management for the Piața.ro marketplace.
"""

import os
import sys
import asyncio
import json
import hashlib
import mimetypes
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from pathlib import Path
import requests
import base64

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'piata_ro.settings')

import django
from django.conf import settings
django.setup()

from django.contrib.auth.models import User
from django.db import transaction, connection
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from asgiref.sync import sync_to_async
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, UploadFile, File
import uvicorn

# Import marketplace models
try:
    from marketplace.models import Listing, Category, ListingImage, UserProfile
    from marketplace.location_services import Location
except ImportError:
    # If marketplace app doesn't exist yet, we'll create placeholder
    Listing = None
    Category = None
    ListingImage = None
    UserProfile = None
    Location = None

# Try to import PIL for image processing
try:
    from PIL import Image, ImageFilter, ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Initialize FastMCP server for content processing
mcp = FastMCP("Content & Media Processing Agent - Piața.ro")

# Create FastAPI app for REST endpoints
rest_app = FastAPI(title="Content & Media Processing API", version="1.0.0")

# Pydantic models for data validation
class UserCreateData(BaseModel):
    username: str
    email: str
    password: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""

class ListingCreateData(BaseModel):
    title: str
    description: str
    price: float
    category_id: int
    user_id: int
    location: str
    contact_info: str
    is_featured: Optional[bool] = False

class UserSearchQuery(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    user_id: Optional[int] = None

class ListingSearchQuery(BaseModel):
    title: Optional[str] = None
    category_id: Optional[int] = None
    location: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    user_id: Optional[int] = None
    is_featured: Optional[bool] = None

# Database connection helper
def get_db_connection():
    """Get Django database connection"""
    return connection

@mcp.tool()
def create_user(user_data: UserCreateData) -> Dict[str, Any]:
    """
    Create a new user in the Django database.
    
    Args:
        user_data: User creation data including username, email, password
        
    Returns:
        Dictionary with user creation status and user info
    """
    try:
        with transaction.atomic():
            # Check if user already exists
            if User.objects.filter(username=user_data.username).exists():
                return {
                    "success": False,
                    "error": f"User with username '{user_data.username}' already exists",
                    "user_id": None
                }
            
            if User.objects.filter(email=user_data.email).exists():
                return {
                    "success": False,
                    "error": f"User with email '{user_data.email}' already exists",
                    "user_id": None
                }
            
            # Create new user
            user = User.objects.create_user(
                username=user_data.username,
                email=user_data.email,
                password=user_data.password,
                first_name=user_data.first_name,
                last_name=user_data.last_name
            )
            
            return {
                "success": True,
                "message": f"User '{user_data.username}' created successfully",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined.isoformat()
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create user: {str(e)}",
            "user_id": None
        }

@mcp.tool()
def get_user_info(search_query: UserSearchQuery) -> Dict[str, Any]:
    """
    Retrieve user information from the database.
    
    Args:
        search_query: Search criteria (username, email, or user_id)
        
    Returns:
        Dictionary with user information or error message
    """
    try:
        user = None
        
        if search_query.user_id:
            user = User.objects.get(id=search_query.user_id)
        elif search_query.username:
            user = User.objects.get(username=search_query.username)
        elif search_query.email:
            user = User.objects.get(email=search_query.email)
        else:
            return {
                "success": False,
                "error": "Please provide username, email, or user_id",
                "user": None
            }
        
        return {
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "date_joined": user.date_joined.isoformat(),
                "last_login": user.last_login.isoformat() if user.last_login else None
            }
        }
        
    except ObjectDoesNotExist:
        return {
            "success": False,
            "error": "User not found",
            "user": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve user: {str(e)}",
            "user": None
        }

@mcp.tool()
def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """
    Authenticate a user with username and password.
    
    Args:
        username: Username
        password: Password
        
    Returns:
        Dictionary with authentication result and user info
    """
    try:
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # Update last login
                user.last_login = datetime.now()
                user.save(update_fields=['last_login'])
                
                return {
                    "success": True,
                    "authenticated": True,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "is_staff": user.is_staff
                    }
                }
            else:
                return {
                    "success": True,
                    "authenticated": False,
                    "error": "User account is disabled",
                    "user": None
                }
        else:
            return {
                "success": True,
                "authenticated": False,
                "error": "Invalid username or password",
                "user": None
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Authentication failed: {str(e)}",
            "authenticated": False,
            "user": None
        }

@mcp.tool()
def create_listing(listing_data: ListingCreateData) -> Dict[str, Any]:
    """
    Create a new marketplace listing.
    
    Args:
        listing_data: Listing creation data
        
    Returns:
        Dictionary with listing creation status and listing info
    """
    try:
        # Import here to avoid circular imports
        from marketplace.models import Listing, Category
        
        with transaction.atomic():
            # Verify user exists
            user = User.objects.get(id=listing_data.user_id)
            
            # Verify category exists
            category = Category.objects.get(id=listing_data.category_id)
            
            # Create listing
            listing = Listing.objects.create(
                title=listing_data.title,
                description=listing_data.description,
                price=listing_data.price,
                category=category,
                user=user,
                location=listing_data.location,
                contact_info=listing_data.contact_info,
                is_featured=listing_data.is_featured
            )
            
            return {
                "success": True,
                "message": f"Listing '{listing_data.title}' created successfully",
                "listing_id": listing.id,
                "title": listing.title,
                "price": float(listing.price),
                "category": listing.category.name,
                "created_at": listing.created_at.isoformat()
            }
            
    except User.DoesNotExist:
        return {
            "success": False,
            "error": f"User with ID {listing_data.user_id} not found",
            "listing_id": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create listing: {str(e)}",
            "listing_id": None
        }

@mcp.tool()
def search_listings(search_query: ListingSearchQuery) -> Dict[str, Any]:
    """
    Search for marketplace listings based on various criteria.
    
    Args:
        search_query: Search criteria for listings
        
    Returns:
        Dictionary with search results
    """
    try:
        from marketplace.models import Listing
        
        # Start with all listings
        queryset = Listing.objects.select_related('category', 'user').all()
        
        # Apply filters
        if search_query.title:
            queryset = queryset.filter(title__icontains=search_query.title)
        
        if search_query.category_id:
            queryset = queryset.filter(category_id=search_query.category_id)
        
        if search_query.location:
            queryset = queryset.filter(location__icontains=search_query.location)
        
        if search_query.min_price is not None:
            queryset = queryset.filter(price__gte=search_query.min_price)
        
        if search_query.max_price is not None:
            queryset = queryset.filter(price__lte=search_query.max_price)
        
        if search_query.user_id:
            queryset = queryset.filter(user_id=search_query.user_id)
        
        if search_query.is_featured is not None:
            queryset = queryset.filter(is_featured=search_query.is_featured)
        
        # Order by creation date (newest first)
        queryset = queryset.order_by('-created_at')
        
        # Limit results to prevent too much data
        listings = queryset[:50]
        
        results = []
        for listing in listings:
            results.append({
                "id": listing.id,
                "title": listing.title,
                "description": listing.description[:200] + "..." if len(listing.description) > 200 else listing.description,
                "price": float(listing.price),
                "category": listing.category.name,
                "location": listing.location,
                "user": listing.user.username,
                "is_featured": listing.is_featured,
                "created_at": listing.created_at.isoformat()
            })
        
        return {
            "success": True,
            "count": len(results),
            "total_found": queryset.count(),
            "listings": results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to search listings: {str(e)}",
            "listings": []
        }

@mcp.tool()
async def get_database_stats() -> Dict[str, Any]:
    """
    Get database statistics and health information.
    
    Returns:
        Dictionary with database statistics
    """
    try:
        from marketplace.models import Listing, Category
        
        # Get counts using sync_to_async
        total_users = await sync_to_async(User.objects.count)()
        active_users = await sync_to_async(User.objects.filter(is_active=True).count)()
        total_listings = await sync_to_async(Listing.objects.count)()
        featured_listings = await sync_to_async(Listing.objects.filter(is_featured=True).count)()
        total_categories = await sync_to_async(Category.objects.count)()
        
        # Get recent activity using sync_to_async
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_users = await sync_to_async(
            User.objects.filter(date_joined__gte=seven_days_ago).count
        )()
        
        recent_listings = await sync_to_async(
            Listing.objects.filter(created_at__gte=seven_days_ago).count
        )()
        
        return {
            "success": True,
            "stats": {
                "users": {
                    "total": total_users,
                    "active": active_users,
                    "recent_registrations": recent_users
                },
                "listings": {
                    "total": total_listings,
                    "featured": featured_listings,
                    "recent_posts": recent_listings
                },
                "categories": {
                    "total": total_categories
                },
                "database_info": {
                    "backend": settings.DATABASES['default']['ENGINE'],
                    "name": settings.DATABASES['default']['NAME']
                }
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get database stats: {str(e)}",
            "stats": {}
        }

@mcp.tool()
def execute_custom_query(query: str, params: Optional[List] = None) -> Dict[str, Any]:
    """
    Execute a custom SQL query (READ ONLY for safety).
    
    Args:
        query: SQL query to execute (SELECT only)
        params: Optional parameters for the query
        
    Returns:
        Dictionary with query results
    """
    try:
        # Security check - only allow SELECT queries
        query_upper = query.strip().upper()
        if not query_upper.startswith('SELECT'):
            return {
                "success": False,
                "error": "Only SELECT queries are allowed for security reasons",
                "results": []
            }
        
        # Check for dangerous keywords
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return {
                    "success": False,
                    "error": f"Query contains dangerous keyword: {keyword}",
                    "results": []
                }
        
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
            columns = [col[0] for col in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
        
        return {
            "success": True,
            "query": query,
            "column_count": len(columns),
            "row_count": len(results),
            "columns": columns,
            "results": results[:100]  # Limit results for safety
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Query execution failed: {str(e)}",
            "results": []
        }

@mcp.tool()
def get_marketplace_context() -> Dict[str, Any]:
    """
    Get comprehensive marketplace context including categories, subcategories, and recent listings.
    
    Returns:
        Dictionary with complete marketplace information
    """
    try:
        from marketplace.models import Listing, Category
        
        # Get categories with hierarchical structure
        main_categories = Category.objects.filter(parent__isnull=True).values(
            'id', 'name', 'slug', 'icon', 'color'
        )
        
        # Get subcategories grouped by parent
        subcategories = {}
        for subcat in Category.objects.filter(parent__isnull=False).values(
            'id', 'name', 'slug', 'parent_id', 'icon', 'color'
        ):
            parent_id = subcat['parent_id']
            if parent_id not in subcategories:
                subcategories[parent_id] = []
            subcategories[parent_id].append(subcat)
        
        # Build complete category structure
        categories_structure = []
        for category in main_categories:
            cat_data = dict(category)
            cat_data['subcategories'] = subcategories.get(category['id'], [])
            cat_data['listings_count'] = Listing.objects.filter(
                category_id__in=[category['id']] + [sub['id'] for sub in cat_data['subcategories']]
            ).count()
            categories_structure.append(cat_data)
        
        # Get overall statistics
        listings_count = Listing.objects.count()
        active_listings = Listing.objects.filter(status='active').count()
        featured_count = Listing.objects.filter(is_featured=True).count()
        
        # Get recent listings for context
        recent_listings = list(Listing.objects.filter(status='active').select_related('category', 'user').values(
            'id', 'title', 'price', 'currency', 'location', 'category__name', 'created_at'
        ).order_by('-created_at')[:20])
        
        # Convert datetime objects to ISO format strings
        for listing in recent_listings:
            if listing['created_at']:
                listing['created_at'] = listing['created_at'].isoformat()
        
        return {
            "success": True,
            "marketplace_context": {
                'categories': list(main_categories),  # Simple format
                'categories_structure': categories_structure,  # Enhanced structure
                'total_listings': listings_count,
                'active_listings': active_listings,
                'featured_listings': featured_count,
                'recent_listings': recent_listings,
                'last_updated': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get marketplace context: {str(e)}",
            "marketplace_context": {}
        }

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
        result = tool_function(**tool_args)
        
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
    return {"status": "healthy", "service": "django-sql-agent"}

# Run the MCP server
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Django SQL Agent MCP Server')
    parser.add_argument('--port', type=int, default=8002, help='Port to run the MCP server on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the MCP server to')
    args = parser.parse_args()
    
    print("🚀 Starting Django SQL Agent MCP Server...")
    print("Available tools:")
    print("  - create_user: Create new users")
    print("  - get_user_info: Retrieve user information")
    print("  - authenticate_user: Authenticate users")
    print("  - create_listing: Create marketplace listings")
    print("  - search_listings: Search for listings")
    print("  - get_database_stats: Get database statistics")
    print("  - execute_custom_query: Execute custom SELECT queries")
    print("  - get_marketplace_context: Get marketplace overview")
    print(f"\n🎯 Django SQL Agent ready for Piata.ro database operations on {args.host}:{args.port}!")
    print(f"📡 REST API available at http://{args.host}:{args.port}/call")
    print(f"🔍 Tools list available at http://{args.host}:{args.port}/tools")
    
    # Run the REST API server using uvicorn
    uvicorn.run(rest_app, host=args.host, port=args.port)
