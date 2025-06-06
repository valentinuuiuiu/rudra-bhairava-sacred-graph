import reflex as rx
import httpx
from typing import List, Dict, Any, Optional

from frontend.state import AppState
from frontend.components.navbar import navbar
from frontend.components.search import search_bar
from frontend.components.categories import category_list
from frontend.components.listings import listings_grid


def index() -> rx.Component:
    """The main page of the app."""
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Find anything you need", size="2xl", margin_top="2em"),
                rx.text(
                    "Browse thousands of listings from sellers across Romania",
                    color="gray.600",
                    font_size="xl",
                ),
                search_bar(),
                category_list(),
                listings_grid(),
                spacing="6",
                padding_y="4",
                width="100%",
                max_width="1200px",
            ),
            padding_x="4",
        ),
        on_mount=AppState.fetch_categories,
        width="100%",
        min_height="100vh",
        spacing="0",
    )
