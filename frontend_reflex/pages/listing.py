"""Pagina de detalii anunț pentru aplicația de marketplace Piata.ro."""

from typing import Any, Dict, List, Optional

import httpx
import reflex as rx

from frontend_reflex.components.footer import footer
from frontend_reflex.components.listing_card import listing_card
from frontend_reflex.components.navbar import navbar
from frontend_reflex.state import State


class ListingState(State):
    """Starea pentru pagina de detalii anunț."""

    listing: Optional[Dict[str, Any]] = None
    similar_listings: List[Dict[str, Any]] = []
    loading: bool = False
    error: Optional[str] = None

    async def fetch_listing(self, listing_id: int):
        """Preia detaliile anunțului de la API."""
        self.loading = True
        self.error = None

        try:
            # Preia anunțul
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://localhost:8000/api/listings/{listing_id}/"
                )
                if response.status_code == 200:
                    self.listing = response.json()

                    # Preia anunțuri similare din aceeași categorie
                    category_id = self.listing.get("category", {}).get("id")
                    if category_id:
                        response = await client.get(
                            f"http://localhost:8000/api/categories/{category_id}/listings/"
                        )
                        if response.status_code == 200:
                            # Exclude anunțul curent și limitează la 3 anunțuri
                            self.similar_listings = [
                                listing
                                for listing in response.json()
                                if listing["id"] != listing_id
                            ][:3]
                else:
                    self.error = (
                        f"Eroare la preluarea anunțului: {response.status_code}"
                    )
        except Exception as e:
            self.error = f"Eroare la preluarea datelor: {str(e)}"

        self.loading = False


def listing() -> rx.Component:
    """Componenta paginii de detalii anunț."""
    return rx.box(
        navbar(),
        rx.cond(
            ListingState.loading,
            rx.center(
                rx.spinner(size="xl"),
                py="20",
            ),
            rx.cond(
                ListingState.error,
                rx.center(
                    rx.alert(
                        rx.alert_icon(),
                        rx.alert_title(ListingState.error),
                        status="error",
                    ),
                    py="20",
                ),
                rx.box(
                    # Detalii anunț
                    rx.box(
                        rx.hstack(
                            rx.box(
                                rx.cond(
                                    rx.len_(ListingState.listing.get("images", [])) > 0,
                                    rx.image(
                                        src=ListingState.listing["images"][0],
                                        width="100%",
                                        height="400px",
                                        object_fit="cover",
                                        border_radius="md",
                                    ),
                                    rx.center(
                                        rx.text("Fără imagine", color="gray.500"),
                                        height="400px",
                                        bg="gray.100",
                                        width="100%",
                                        border_radius="md",
                                    ),
                                ),
                                width="60%",
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.heading(
                                        ListingState.listing["title"], size="lg"
                                    ),
                                    rx.text(
                                        f"{ListingState.listing['price']:,.2f} {ListingState.listing['currency']}",
                                        font_weight="bold",
                                        color="blue.500",
                                        font_size="2xl",
                                    ),
                                    rx.hstack(
                                        rx.icon("location_on", color="gray.500"),
                                        rx.text(ListingState.listing["location"]),
                                    ),
                                    rx.divider(),
                                    rx.vstack(
                                        rx.heading("Informații vânzător", size="sm"),
                                        rx.hstack(
                                            rx.avatar(size="md"),
                                            rx.vstack(
                                                rx.text(
                                                    ListingState.listing["user"][
                                                        "username"
                                                    ],
                                                    font_weight="bold",
                                                ),
                                                rx.text(
                                                    "Membru din 2025",
                                                    color="gray.500",
                                                    font_size="sm",
                                                ),
                                                align_items="start",
                                            ),
                                            align="center",
                                        ),
                                        rx.button(
                                            "Contactează vânzătorul",
                                            color_scheme="blue",
                                            width="100%",
                                            mt="4",
                                        ),
                                        rx.button(
                                            rx.hstack(
                                                rx.icon("favorite"),
                                                rx.text("Adaugă la favorite"),
                                            ),
                                            variant="outline",
                                            width="100%",
                                            mt="2",
                                        ),
                                        align_items="start",
                                        width="100%",
                                        p="4",
                                        border="1px solid",
                                        border_color="gray.200",
                                        border_radius="md",
                                    ),
                                    align_items="start",
                                    height="100%",
                                    spacing="4",
                                ),
                                width="40%",
                            ),
                            align_items="start",
                            spacing="8",
                            width="100%",
                        ),
                        # Descriere anunț
                        rx.box(
                            rx.vstack(
                                rx.heading("Descriere", size="md"),
                                rx.text(ListingState.listing["description"]),
                                align_items="start",
                                spacing="4",
                                p="6",
                                border="1px solid",
                                border_color="gray.200",
                                border_radius="md",
                            ),
                            mt="8",
                        ),
                        # Detalii suplimentare
                        rx.box(
                            rx.vstack(
                                rx.heading("Detalii", size="md"),
                                rx.grid(
                                    rx.grid_item(
                                        rx.hstack(
                                            rx.text("Categorie:", font_weight="bold"),
                                            rx.text(
                                                ListingState.listing["category"]["name"]
                                            ),
                                        ),
                                    ),
                                    rx.grid_item(
                                        rx.hstack(
                                            rx.text("Publicat la:", font_weight="bold"),
                                            rx.text(
                                                ListingState.listing[
                                                    "created_at"
                                                ].split("T")[0]
                                            ),
                                        ),
                                    ),
                                    rx.grid_item(
                                        rx.hstack(
                                            rx.text("Vizualizări:", font_weight="bold"),
                                            rx.text(str(ListingState.listing["views"])),
                                        ),
                                    ),
                                    rx.grid_item(
                                        rx.hstack(
                                            rx.text("ID anunț:", font_weight="bold"),
                                            rx.text(str(ListingState.listing["id"])),
                                        ),
                                    ),
                                    template_columns="repeat(2, 1fr)",
                                    gap="4",
                                    width="100%",
                                ),
                                align_items="start",
                                spacing="4",
                                p="6",
                                border="1px solid",
                                border_color="gray.200",
                                border_radius="md",
                            ),
                            mt="8",
                        ),
                        # Anunțuri similare
                        rx.cond(
                            rx.len_(ListingState.similar_listings) > 0,
                            rx.box(
                                rx.vstack(
                                    rx.heading("Anunțuri similare", size="md", mb="4"),
                                    rx.wrap(
                                        rx.foreach(
                                            ListingState.similar_listings,
                                            lambda listing: listing_card(
                                                id=listing["id"],
                                                title=listing["title"],
                                                price=listing["price"],
                                                currency=listing["currency"],
                                                location=listing["location"],
                                                image=(
                                                    listing["images"][0]
                                                    if listing["images"]
                                                    else None
                                                ),
                                            ),
                                        ),
                                        spacing="4",
                                        justify="start",
                                    ),
                                    align_items="start",
                                    width="100%",
                                ),
                                mt="12",
                            ),
                        ),
                        max_width="1200px",
                        mx="auto",
                        px="4",
                        py="10",
                    ),
                ),
            ),
        ),
        footer(),
        on_mount=lambda: ListingState.fetch_listing(
            rx.State.router.page.params.get("id", 1)
        ),
    )
