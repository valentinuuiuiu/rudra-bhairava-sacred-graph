import reflex as rx

from frontend_reflex.state import AppState


def listing_card(listing) -> rx.Component:
    """A card component for a listing."""
    return rx.link(
        rx.box(
            rx.vstack(
                rx.image(
                    src=(
                        listing["images"][0]
                        if listing["images"] and len(listing["images"]) > 0
                        else "https://via.placeholder.com/300x200?text=No+Image"
                    ),
                    height="200px",
                    width="100%",
                    object_fit="cover",
                ),
                rx.vstack(
                    rx.heading(listing["title"], size="md"),
                    rx.text(
                        (
                            f"{listing['price']} {listing['currency']}"
                            if listing.get("price")
                            else "Price on request"
                        ),
                        color="blue.500",
                        font_weight="bold",
                    ),
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
            transition="transform 0.2s, box-shadow 0.2s",
            _hover={
                "transform": "translateY(-5px)",
                "box_shadow": "lg",
            },
        ),
        href=f"/listing/{listing['id']}",
        text_decoration="none",
        color="inherit",
    )


def listings_grid() -> rx.Component:
    """The listings grid component."""
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
                lambda: len(AppState.listings) == 0,
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
