import reflex as rx

from frontend_reflex.components.navbar import navbar
from frontend_reflex.state import ListingState


def listing() -> rx.Component:
    """The listing detail page."""
    return rx.vstack(
        navbar(),
        rx.container(
            rx.cond(
                ListingState.loading,
                rx.center(
                    rx.spinner(size="xl"),
                    padding="10",
                ),
                rx.cond(
                    ListingState.error,
                    rx.box(
                        rx.text(ListingState.error, color="red.500"),
                        padding="10",
                    ),
                    rx.cond(
                        lambda: ListingState.listing is None,
                        rx.center(
                            rx.text("Listing not found", color="gray.500"),
                            padding="10",
                        ),
                        rx.vstack(
                            rx.hstack(
                                rx.link(
                                    "← Back to listings",
                                    href="/",
                                    color="blue.500",
                                ),
                                rx.spacer(),
                                width="100%",
                            ),
                            rx.heading(ListingState.listing["title"], size="xl"),
                            rx.hstack(
                                rx.text(
                                    (
                                        f"{ListingState.listing['price']} {ListingState.listing['currency']}"
                                        if ListingState.listing.get("price")
                                        else "Price on request"
                                    ),
                                    color="blue.500",
                                    font_weight="bold",
                                    font_size="2xl",
                                ),
                                rx.spacer(),
                                rx.text(
                                    f"Location: {ListingState.listing['location']}",
                                    color="gray.600",
                                ),
                                width="100%",
                            ),
                            rx.cond(
                                lambda: ListingState.listing.get("images")
                                and len(ListingState.listing["images"]) > 0,
                                rx.image(
                                    src=ListingState.listing["images"][0],
                                    height="400px",
                                    width="100%",
                                    object_fit="cover",
                                    border_radius="md",
                                ),
                                rx.box(
                                    rx.text("No image available", color="gray.500"),
                                    height="400px",
                                    width="100%",
                                    background_color="gray.100",
                                    border_radius="md",
                                    display="flex",
                                    justify_content="center",
                                    align_items="center",
                                ),
                            ),
                            rx.box(
                                rx.heading("Description", size="lg", margin_top="1em"),
                                rx.text(ListingState.listing["description"]),
                                width="100%",
                            ),
                            rx.box(
                                rx.heading(
                                    "Contact Seller", size="lg", margin_top="1em"
                                ),
                                rx.hstack(
                                    rx.avatar(
                                        name=ListingState.listing["user"]["username"],
                                        src=ListingState.listing["user"].get(
                                            "avatar", ""
                                        ),
                                        size="lg",
                                    ),
                                    rx.vstack(
                                        rx.text(
                                            ListingState.listing["user"]["username"],
                                            font_weight="bold",
                                        ),
                                        rx.text(
                                            f"Member since {ListingState.listing['user']['date_joined'].split('T')[0]}",
                                            color="gray.600",
                                            font_size="sm",
                                        ),
                                        align_items="start",
                                    ),
                                    spacing="4",
                                    align_items="center",
                                ),
                                rx.button(
                                    "Contact Seller",
                                    color_scheme="blue",
                                    width="100%",
                                    margin_top="1em",
                                ),
                                width="100%",
                                padding="4",
                                border="1px solid",
                                border_color="gray.200",
                                border_radius="md",
                                margin_top="1em",
                            ),
                            spacing="4",
                            width="100%",
                            max_width="800px",
                            padding_y="4",
                        ),
                    ),
                ),
            ),
            padding_x="4",
            width="100%",
        ),
        on_mount=lambda: ListingState.set_listing_id(
            rx.get_query_params().get("id", "")
        ),
        width="100%",
        min_height="100vh",
        spacing="0",
    )
