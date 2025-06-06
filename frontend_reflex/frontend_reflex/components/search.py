import reflex as rx

from frontend_reflex.state import AppState


def search_bar() -> rx.Component:
    """The search bar component."""
    return rx.hstack(
        rx.input(
            placeholder="What are you looking for?",
            on_change=AppState.set_search_query,
            value=AppState.search_query,
            width="100%",
            size="lg",
            border_radius="md",
        ),
        rx.button(
            "Search",
            on_click=AppState.search,
            color_scheme="blue",
            size="lg",
        ),
        width="100%",
        spacing="2",
    )
