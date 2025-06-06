import reflex as rx
import httpx
from typing import List, Dict, Any, Optional

# API URL
API_URL = "http://localhost:8000/api"

# State
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
                    self.listings = response.json()
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


# Components
def navbar():
    return rx.hstack(
        rx.heading("Piata.ro", size="lg", color="blue.500"),
        rx.spacer(),
        rx.hstack(
            rx.link("Home", href="/", color="gray.800"),
            rx.link("My Account", href="/account", color="gray.800"),
            rx.link("Post Ad", href="/post", color="gray.800"),
            rx.link("Favorites", href="/favorites", color="gray.800"),
            rx.link("Messages", href="/messages", color="gray.800"),
            spacing="4",
        ),
        width="100%",
        padding="4",
        border_bottom="1px solid",
        border_color="gray.200",
    )


def search_bar():
    return rx.hstack(
        rx.input(
            placeholder="What are you looking for?",
            on_change=AppState.set_search_query,
            value=AppState.search_query,
            width="100%",
        ),
        rx.button(
            "Search",
            on_click=AppState.search,
            color_scheme="blue",
        ),
        width="100%",
        padding="4",
    )


def category_list():
    return rx.scroll_area(
        rx.hstack(
            rx.button(
                "All Categories",
                on_click=lambda: AppState.set_category(None),
                variant="ghost",
                color_scheme="blue" if AppState.selected_category is None else "gray",
            ),
            rx.foreach(
                AppState.categories,
                lambda category: rx.button(
                    category["name"],
                    on_click=lambda: AppState.set_category(category["id"]),
                    variant="ghost",
                    color_scheme="blue" if AppState.selected_category == category["id"] else "gray",
                ),
            ),
            spacing="2",
            overflow_x="auto",
            padding="2",
        ),
        orientation="horizontal",
        width="100%",
    )


def listing_card(listing):
    return rx.box(
        rx.vstack(
            rx.image(
                src=listing["images"][0] if listing["images"] else "https://via.placeholder.com/300x200?text=No+Image",
                height="200px",
                width="100%",
                object_fit="cover",
            ),
            rx.vstack(
                rx.heading(listing["title"], size="md"),
                rx.text(f"{listing['price']} {listing['currency']}", color="blue.500", font_weight="bold"),
                rx.text(listing["location"], color="gray.500"),
                align_items="start",
                padding="4",
                spacing="1",
            ),
            spacing="0",
            align_items="start",
            width="100%",
        ),
        border="1px solid",
        border_color="gray.200",
        border_radius="md",
        overflow="hidden",
        width="100%",
    )


def listings_grid():
    return rx.cond(
        AppState.loading,
        rx.center(
            rx.spinner(size="xl"),
            padding="10",
        ),
        rx.cond(
            AppState.error,
            rx.box(
                rx.text(AppState.error, color="red.500"),
                padding="10",
            ),
            rx.cond(
                len(AppState.listings) == 0,
                rx.center(
                    rx.text("No listings found", color="gray.500"),
                    padding="10",
                ),
                rx.grid(
                    rx.foreach(
                        AppState.listings,
                        listing_card,
                    ),
                    columns=[1, 2, 3, 4],
                    gap="4",
                    padding="4",
                ),
            ),
        ),
    )


# Pages
def index():
    return rx.vstack(
        navbar(),
        search_bar(),
        category_list(),
        listings_grid(),
        on_mount=AppState.fetch_categories,
        width="100%",
        spacing="0",
    )


# Create the app
app = rx.App()
app.add_page(index)
