"""Componenta card anunț pentru Piata.ro."""

import reflex as rx
from typing import Optional
from datetime import datetime


def listing_card(
    id: int,
    title: str,
    price: float,
    currency: str = "lei",
    location: str = "",
    image: Optional[str] = None,
    created_at: Optional[str] = None,
    is_featured: bool = False,
) -> rx.Component:
    """Card pentru afișarea unui anunț în stil publi24.ro."""
    # Formatare preț
    formatted_price = f"{price:,.0f} {currency}" if price else "Preț negociabil"

    # Formatare dată
    date_display = ""
    if created_at:
        try:
            date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            date_display = date_obj.strftime("%d %b %Y")
        except (ValueError, AttributeError):
            date_display = created_at

    return rx.link(
        rx.box(
            # Imagine anunț
            rx.cond(
                image,
                rx.image(
                    src=image,
                    height="180px",
                    width="100%",
                    object_fit="cover",
                    alt=title,
                    border_top_radius="md",
                ),
                rx.center(
                    rx.icon("image", color="gray.400", size="xl"),
                    height="180px",
                    bg="gray.100",
                    width="100%",
                    border_top_radius="md",
                ),
            ),

            # Conținut anunț
            rx.box(
                # Titlu anunț
                rx.heading(
                    title,
                    size="sm",
                    mb="2",
                    no_of_lines=2,
                    font_weight="600",
                ),

                # Preț
                rx.text(
                    formatted_price,
                    font_weight="bold",
                    color="blue.500",
                    font_size="lg",
                    mb="1",
                ),

                # Locație
                rx.hstack(
                    rx.icon("map-pin", size="xs", color="gray.500"),
                    rx.text(
                        location,
                        color="gray.500",
                        font_size="sm",
                    ),
                    spacing="1",
                    mb="1",
                ),

                # Data publicării
                rx.text(
                    date_display,
                    color="gray.500",
                    font_size="xs",
                    mb="3",
                ),

                # Buton vezi detalii
                rx.button(
                    "Vezi detalii",
                    size="sm",
                    width="100%",
                    color_scheme="blue",
                    variant="outline",
                ),

                p="4",
            ),

            # Badge pentru anunțuri promovate
            rx.cond(
                is_featured,
                rx.badge(
                    "Promovat",
                    color_scheme="orange",
                    position="absolute",
                    top="2",
                    right="2",
                ),
            ),

            border="1px solid",
            border_color="gray.200",
            border_radius="md",
            overflow="hidden",
            bg="white",
            position="relative",
            height="100%",
            _hover={
                "transform": "translateY(-5px)",
                "shadow": "lg",
            },
            transition="all 0.3s",
        ),
        href=f"/listing/{id}",
        _hover={"text_decoration": "none"},
        width="100%",
        max_width="280px",
        height="100%",
    )
