"""Pagina principală pentru aplicația de marketplace Piata.ro."""

from typing import Any, Dict, List, Optional

import httpx
import reflex as rx

from frontend_reflex.components.category_card import category_card
from frontend_reflex.components.footer import footer
from frontend_reflex.components.listing_card import listing_card
from frontend_reflex.components.navbar import navbar
from frontend_reflex.state import State


class HomeState(State):
    """Starea pentru pagina principală."""

    categories: List[Dict[str, Any]] = []
    listings: List[Dict[str, Any]] = []
    loading: bool = False
    error: Optional[str] = None

    async def fetch_data(self):
        """Preia categoriile și anunțurile de la API."""
        self.loading = True
        self.error = None

        try:
            # Preia categoriile
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/categories/")
                if response.status_code == 200:
                    self.categories = response.json()
                else:
                    self.error = (
                        f"Eroare la preluarea categoriilor: {response.status_code}"
                    )

                # Preia anunțurile
                response = await client.get("http://localhost:8000/api/listings/")
                if response.status_code == 200:
                    self.listings = response.json()[:6]  # Preia doar primele 6 anunțuri
                else:
                    self.error = (
                        f"Eroare la preluarea anunțurilor: {response.status_code}"
                    )
        except Exception as e:
            self.error = f"Eroare la preluarea datelor: {str(e)}"

        self.loading = False


def index() -> rx.Component:
    """Componenta paginii principale."""
    return rx.box(
        navbar(),
        # Secțiunea hero
        rx.box(
            rx.vstack(
                rx.heading("Bine ați venit la Piata.ro", size="2xl", mb=4),
                rx.text(
                    "Cel mai bun marketplace pentru cumpărare și vânzare în România",
                    mb=8,
                    font_size="xl",
                ),
                rx.form(
                    rx.hstack(
                        rx.input(
                            placeholder="Ce căutați?",
                            size="lg",
                            width="100%",
                        ),
                        rx.button("Caută", color_scheme="blue", size="lg"),
                    ),
                    width="100%",
                    max_width="600px",
                ),
                align="center",
                spacing="4",
                py="20",
                text_align="center",
            ),
            bg="gray.50",
            width="100%",
        ),
        # Secțiunea categorii
        rx.box(
            rx.vstack(
                rx.heading("Categorii populare", size="xl", mb=8),
                rx.cond(
                    HomeState.loading,
                    rx.center(rx.spinner(size="xl")),
                    rx.cond(
                        HomeState.error,
                        rx.alert(
                            rx.alert_icon(),
                            rx.alert_title(HomeState.error),
                            status="error",
                        ),
                        rx.wrap(
                            rx.foreach(
                                HomeState.categories,
                                lambda category: category_card(
                                    name=category["name"],
                                    id=category["id"],
                                ),
                            ),
                            spacing="4",
                            justify="center",
                        ),
                    ),
                ),
                width="100%",
                py="10",
            ),
            max_width="1200px",
            mx="auto",
            px="4",
        ),
        # Secțiunea anunțuri
        rx.box(
            rx.vstack(
                rx.heading("Ultimele anunțuri", size="xl", mb=8),
                rx.cond(
                    HomeState.loading,
                    rx.center(rx.spinner(size="xl")),
                    rx.cond(
                        HomeState.error,
                        rx.alert(
                            rx.alert_icon(),
                            rx.alert_title(HomeState.error),
                            status="error",
                        ),
                        rx.wrap(
                            rx.foreach(
                                HomeState.listings,
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
                            justify="center",
                        ),
                    ),
                ),
                width="100%",
                py="10",
            ),
            max_width="1200px",
            mx="auto",
            px="4",
        ),
        # Secțiunea caracteristici
        rx.box(
            rx.vstack(
                rx.heading("De ce să alegeți Piata.ro?", size="xl", mb=8),
                rx.hstack(
                    rx.vstack(
                        rx.text("🔒", font_size="4xl", mb=2),
                        rx.heading("Tranzacții sigure", size="md", mb=2),
                        rx.text(
                            "Platforma noastră asigură tranzacții sigure și securizate."
                        ),
                        align="center",
                        p="6",
                        border_radius="md",
                        border_width="1px",
                        border_color="gray.200",
                    ),
                    rx.vstack(
                        rx.text("👥", font_size="4xl", mb=2),
                        rx.heading("Utilizatori verificați", size="md", mb=2),
                        rx.text(
                            "Toți utilizatorii sunt verificați pentru a asigura o comunitate de încredere."
                        ),
                        align="center",
                        p="6",
                        border_radius="md",
                        border_width="1px",
                        border_color="gray.200",
                    ),
                    rx.vstack(
                        rx.text("🚀", font_size="4xl", mb=2),
                        rx.heading("Rapid și ușor", size="md", mb=2),
                        rx.text(
                            "Publicați anunțul în câteva minute și ajungeți la mii de cumpărători potențiali."
                        ),
                        align="center",
                        p="6",
                        border_radius="md",
                        border_width="1px",
                        border_color="gray.200",
                    ),
                    spacing="4",
                    wrap="wrap",
                    justify="center",
                ),
                width="100%",
                py="10",
            ),
            max_width="1200px",
            mx="auto",
            px="4",
            bg="gray.50",
        ),
        footer(),
        on_mount=HomeState.fetch_data,
    )
