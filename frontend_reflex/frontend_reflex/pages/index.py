import reflex as rx

from frontend_reflex.components.categories import category_list
from frontend_reflex.components.listings import listings_grid
from frontend_reflex.components.navbar import navbar
from frontend_reflex.components.search import search_bar
from frontend_reflex.state import AppState


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
