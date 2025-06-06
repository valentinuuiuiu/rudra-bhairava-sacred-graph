import reflex as rx
import httpx
from typing import List, Dict, Any, Optional

# API URL
API_URL = "http://localhost:8000/api"

class AppState(rx.State):
    """The app state."""
    # Data
    categories: List[Dict[str, Any]] = []
    listings: List[Dict[str, Any]] = []
    selected_category: Optional[int] = None
    search_query: str = ""
    loading: bool = False
    error: Optional[str] = None
    
    # Fetch categories
    async def fetch_categories(self):
        self.loading = True
        self.error = None
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/categories/")
                if response.status_code == 200:
                    self.categories = response.json()
                else:
                    self.error = f"Error fetching categories: {response.status_code}"
        except Exception as e:
            self.error = f"Error: {str(e)}"
        finally:
            self.loading = False
            # After fetching categories, fetch listings
            await self.fetch_listings()
    
    # Fetch listings
    async def fetch_listings(self):
        self.loading = True
        self.error = None
        
        # Build query parameters
        params = {}
        if self.selected_category:
            params["category"] = self.selected_category
        if self.search_query:
            params["search"] = self.search_query
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/listings/", params=params)
                if response.status_code == 200:
                    data = response.json()
                    self.listings = data.get("results", [])
                else:
                    self.error = f"Error fetching listings: {response.status_code}"
        except Exception as e:
            self.error = f"Error: {str(e)}"
        finally:
            self.loading = False
    
    # Set selected category
    def set_category(self, category_id: Optional[int]):
        self.selected_category = category_id
        return self.fetch_listings
    
    # Set search query
    def set_search_query(self, query: str):
        self.search_query = query
    
    # Search listings
    def search(self):
        return self.fetch_listings


class ListingState(rx.State):
    """The listing detail page state."""
    # Data
    listing_id: Optional[str] = None
    listing: Optional[Dict[str, Any]] = None
    loading: bool = False
    error: Optional[str] = None
    
    def set_listing_id(self, listing_id: str):
        """Set the listing ID and fetch the listing details."""
        self.listing_id = listing_id
        return self.fetch_listing
    
    async def fetch_listing(self):
        """Fetch the listing details from the API."""
        if not self.listing_id:
            self.error = "No listing ID provided"
            return
        
        self.loading = True
        self.error = None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/listings/{self.listing_id}/")
                if response.status_code == 200:
                    self.listing = response.json()
                else:
                    self.error = f"Error fetching listing: {response.status_code}"
        except Exception as e:
            self.error = f"Error: {str(e)}"
        finally:
            self.loading = False


class AuthState(rx.State):
    """Authentication state."""
    # Data
    token: Optional[str] = None
    user: Optional[Dict[str, Any]] = None
    loading: bool = False
    error: Optional[str] = None
    
    # Login
    async def login(self, username: str, password: str):
        self.loading = True
        self.error = None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/token/",
                    data={"username": username, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    self.token = data.get("access")
                    await self.fetch_user()
                else:
                    self.error = "Invalid username or password"
        except Exception as e:
            self.error = f"Error: {str(e)}"
        finally:
            self.loading = False
    
    # Fetch user
    async def fetch_user(self):
        if not self.token:
            self.error = "Not authenticated"
            return
        
        self.loading = True
        self.error = None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{API_URL}/users/me/",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                if response.status_code == 200:
                    self.user = response.json()
                else:
                    self.error = f"Error fetching user: {response.status_code}"
        except Exception as e:
            self.error = f"Error: {str(e)}"
        finally:
            self.loading = False
    
    # Logout
    def logout(self):
        self.token = None
        self.user = None
