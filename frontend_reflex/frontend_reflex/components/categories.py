import reflex as rx
from frontend_reflex.state import AppState

def category_list() -> rx.Component:
    """The category list component."""
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
                    on_click=lambda c=category: AppState.set_category(c["id"]),
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
