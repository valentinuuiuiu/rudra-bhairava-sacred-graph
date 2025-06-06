"""Piata.ro - O aplicație de marketplace modernă construită cu Reflex."""

import reflex as rx
from typing import List, Dict, Any, Optional
import httpx


class MarketplaceState(rx.State):
    """Starea aplicației de marketplace."""
    
    # Date
    categories: List[Dict[str, Any]] = []
    featured_listings: List[Dict[str, Any]] = []
    latest_listings: List[Dict[str, Any]] = []
    
    # UI state
    is_loading: bool = False
    error: Optional[str] = None
    search_query: str = ""
    
    # User state
    is_authenticated: bool = False
    username: Optional[str] = None
    
    async def fetch_data(self):
        """Preia datele de la API-ul Django."""
        self.is_loading = True
        self.error = None
        
        try:
            # Preia categoriile
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/categories/")
                if response.status_code == 200:
                    self.categories = response.json()
                else:
                    self.error = f"Eroare la preluarea categoriilor: {response.status_code}"
                
                # Preia anunțurile recente
                response = await client.get("http://localhost:8000/api/listings/")
                if response.status_code == 200:
                    listings = response.json()
                    self.latest_listings = listings[:6]  # Primele 6 anunțuri
                    
                    # Filtrează anunțurile premium pentru secțiunea featured
                    self.featured_listings = [
                        listing for listing in listings 
                        if listing.get("is_premium", False)
                    ][:3]
                    
                    # Dacă nu avem anunțuri premium, folosim primele 3 anunțuri
                    if not self.featured_listings:
                        self.featured_listings = listings[:3]
                else:
                    self.error = f"Eroare la preluarea anunțurilor: {response.status_code}"
        except Exception as e:
            self.error = f"Eroare la preluarea datelor: {str(e)}"
        
        self.is_loading = False
    
    def search(self):
        """Efectuează o căutare."""
        return rx.redirect(f"/search?q={self.search_query}")


# Componente
def navbar() -> rx.Component:
    """Bara de navigare."""
    return rx.chakra.box(
        rx.chakra.hstack(
            rx.chakra.hstack(
                rx.chakra.heading("Piata.ro", size="md", color="blue.500"),
                spacing="2",
                as_="a",
                href="/",
                _hover={"text_decoration": "none"},
            ),
            rx.chakra.spacer(),
            rx.chakra.hstack(
                rx.chakra.menu(
                    rx.chakra.menu_button(
                        "Categorii",
                        right_icon=rx.chakra.icon("chevron_down"),
                    ),
                    rx.chakra.menu_list(
                        rx.foreach(
                            MarketplaceState.categories,
                            lambda category: rx.chakra.menu_item(
                                category["name"],
                                as_="a",
                                href=f"/category/{category['id']}",
                            ),
                        ),
                    ),
                ),
                rx.chakra.link("Anunțuri", href="/listings", color="gray.700"),
                rx.chakra.link("Despre noi", href="/about", color="gray.700"),
                rx.chakra.link("Contact", href="/contact", color="gray.700"),
                spacing="6",
                display=["none", "none", "flex"],
            ),
            rx.chakra.spacer(),
            rx.chakra.cond(
                MarketplaceState.is_authenticated,
                rx.chakra.hstack(
                    rx.chakra.menu(
                        rx.chakra.menu_button(
                            rx.chakra.hstack(
                                rx.chakra.avatar(size="sm"),
                                rx.chakra.text(MarketplaceState.username),
                                spacing="2",
                            ),
                        ),
                        rx.chakra.menu_list(
                            rx.chakra.menu_item("Profilul meu", as_="a", href="/profile"),
                            rx.chakra.menu_item("Anunțurile mele", as_="a", href="/my-listings"),
                            rx.chakra.menu_item("Favorite", as_="a", href="/favorites"),
                            rx.chakra.menu_item("Mesaje", as_="a", href="/messages"),
                            rx.chakra.menu_divider(),
                            rx.chakra.menu_item("Deconectare", on_click=MarketplaceState.logout),
                        ),
                    ),
                    rx.chakra.button(
                        "Adaugă anunț",
                        color_scheme="blue",
                        as_="a",
                        href="/add-listing",
                    ),
                    spacing="4",
                ),
                rx.chakra.hstack(
                    rx.chakra.button("Autentificare", variant="ghost", as_="a", href="/login"),
                    rx.chakra.button("Înregistrare", color_scheme="blue", as_="a", href="/register"),
                    spacing="2",
                ),
            ),
            width="100%",
            py="4",
            px="8",
        ),
        position="sticky",
        top="0",
        z_index="999",
        bg="white",
        border_bottom="1px solid",
        border_color="gray.200",
        width="100%",
    )


def hero_section() -> rx.Component:
    """Secțiunea hero."""
    return rx.chakra.box(
        rx.chakra.container(
            rx.chakra.vstack(
                rx.chakra.heading(
                    "Cumpără și vinde în România",
                    size="2xl",
                    font_weight="bold",
                    color="white",
                    text_align="center",
                ),
                rx.chakra.text(
                    "Cel mai mare marketplace din România",
                    font_size="xl",
                    color="white",
                    text_align="center",
                    mb="8",
                ),
                rx.chakra.hstack(
                    rx.chakra.input(
                        placeholder="Ce cauți?",
                        size="lg",
                        bg="white",
                        border_radius="md",
                        width="100%",
                        value=MarketplaceState.search_query,
                        on_change=MarketplaceState.set_search_query,
                    ),
                    rx.chakra.button(
                        "Caută",
                        color_scheme="blue",
                        size="lg",
                        on_click=MarketplaceState.search,
                    ),
                    width=["100%", "100%", "600px"],
                ),
                spacing="6",
                py="20",
                align_items="center",
            ),
            max_width="container.xl",
        ),
        background="linear-gradient(to right, #1a365d, #3182ce)",
        width="100%",
    )


def category_card(category: Dict[str, Any]) -> rx.Component:
    """Card pentru categorie."""
    return rx.chakra.link(
        rx.chakra.vstack(
            rx.chakra.circle(
                rx.chakra.icon(
                    "category",
                    size="xl",
                    color="blue.500",
                ),
                size="16",
                bg="blue.50",
            ),
            rx.chakra.text(
                category["name"],
                font_weight="bold",
                color="gray.700",
            ),
            spacing="3",
            p="6",
            border_radius="lg",
            border="1px solid",
            border_color="gray.200",
            _hover={
                "transform": "translateY(-5px)",
                "shadow": "md",
                "border_color": "blue.200",
            },
            transition="all 0.3s",
            align="center",
        ),
        href=f"/category/{category['id']}",
        _hover={"text_decoration": "none"},
    )


def listing_card(listing: Dict[str, Any]) -> rx.Component:
    """Card pentru anunț."""
    return rx.chakra.link(
        rx.chakra.box(
            rx.chakra.box(
                rx.chakra.cond(
                    rx.cond(
                        rx.len_(listing.get("images", [])) > 0,
                        True,
                        False,
                    ),
                    rx.chakra.image(
                        src=listing["images"][0],
                        alt=listing["title"],
                        width="100%",
                        height="200px",
                        object_fit="cover",
                        border_top_radius="lg",
                    ),
                    rx.chakra.center(
                        rx.chakra.icon("image", size="4xl", color="gray.300"),
                        height="200px",
                        bg="gray.100",
                        width="100%",
                        border_top_radius="lg",
                    ),
                ),
                rx.chakra.cond(
                    listing.get("is_premium", False),
                    rx.chakra.badge(
                        "Premium",
                        position="absolute",
                        top="2",
                        right="2",
                        color_scheme="yellow",
                    ),
                ),
            ),
            rx.chakra.box(
                rx.chakra.vstack(
                    rx.chakra.heading(
                        listing["title"],
                        size="md",
                        no_of_lines=2,
                    ),
                    rx.chakra.hstack(
                        rx.chakra.text(
                            f"{listing['price']:,.2f} {listing['currency']}",
                            font_weight="bold",
                            color="blue.500",
                            font_size="lg",
                        ),
                        rx.chakra.spacer(),
                        rx.chakra.badge(listing["status"].capitalize()),
                        width="100%",
                    ),
                    rx.chakra.hstack(
                        rx.chakra.icon("location_on", size="sm", color="gray.500"),
                        rx.chakra.text(
                            listing["location"],
                            color="gray.500",
                            font_size="sm",
                        ),
                        width="100%",
                    ),
                    rx.chakra.spacer(),
                    rx.chakra.hstack(
                        rx.chakra.button(
                            "Vezi detalii",
                            size="sm",
                            width="100%",
                            color_scheme="blue",
                            variant="outline",
                        ),
                        rx.chakra.icon_button(
                            "favorite",
                            aria_label="Adaugă la favorite",
                            size="sm",
                            color_scheme="red",
                            variant="ghost",
                        ),
                        width="100%",
                    ),
                    align_items="start",
                    height="100%",
                    p="4",
                    spacing="3",
                ),
            ),
            border_radius="lg",
            overflow="hidden",
            border="1px solid",
            border_color="gray.200",
            height="100%",
            position="relative",
            _hover={
                "transform": "translateY(-5px)",
                "shadow": "md",
            },
            transition="all 0.3s",
        ),
        href=f"/listing/{listing['id']}",
        _hover={"text_decoration": "none"},
    )


def featured_listings_section() -> rx.Component:
    """Secțiunea de anunțuri promovate."""
    return rx.chakra.box(
        rx.chakra.container(
            rx.chakra.vstack(
                rx.chakra.heading(
                    "Anunțuri promovate",
                    size="xl",
                    mb="8",
                ),
                rx.chakra.cond(
                    MarketplaceState.is_loading,
                    rx.chakra.center(
                        rx.chakra.spinner(size="xl"),
                        py="20",
                    ),
                    rx.chakra.cond(
                        rx.len_(MarketplaceState.featured_listings) > 0,
                        rx.chakra.simple_grid(
                            rx.foreach(
                                MarketplaceState.featured_listings,
                                listing_card,
                            ),
                            columns=[1, 2, 3],
                            spacing="6",
                            width="100%",
                        ),
                        rx.chakra.center(
                            rx.chakra.text(
                                "Nu există anunțuri promovate momentan.",
                                color="gray.500",
                            ),
                            py="10",
                        ),
                    ),
                ),
                width="100%",
                py="10",
                spacing="6",
            ),
            max_width="container.xl",
        ),
    )


def categories_section() -> rx.Component:
    """Secțiunea de categorii."""
    return rx.chakra.box(
        rx.chakra.container(
            rx.chakra.vstack(
                rx.chakra.heading(
                    "Categorii populare",
                    size="xl",
                    mb="8",
                ),
                rx.chakra.cond(
                    MarketplaceState.is_loading,
                    rx.chakra.center(
                        rx.chakra.spinner(size="xl"),
                        py="20",
                    ),
                    rx.chakra.simple_grid(
                        rx.foreach(
                            MarketplaceState.categories,
                            category_card,
                        ),
                        columns=[2, 3, 4, 6],
                        spacing="6",
                        width="100%",
                    ),
                ),
                width="100%",
                py="10",
                spacing="6",
            ),
            max_width="container.xl",
        ),
        bg="gray.50",
    )


def latest_listings_section() -> rx.Component:
    """Secțiunea de anunțuri recente."""
    return rx.chakra.box(
        rx.chakra.container(
            rx.chakra.vstack(
                rx.chakra.hstack(
                    rx.chakra.heading(
                        "Anunțuri recente",
                        size="xl",
                    ),
                    rx.chakra.spacer(),
                    rx.chakra.button(
                        "Vezi toate",
                        variant="link",
                        color_scheme="blue",
                        as_="a",
                        href="/listings",
                    ),
                    width="100%",
                ),
                rx.chakra.cond(
                    MarketplaceState.is_loading,
                    rx.chakra.center(
                        rx.chakra.spinner(size="xl"),
                        py="20",
                    ),
                    rx.chakra.cond(
                        rx.len_(MarketplaceState.latest_listings) > 0,
                        rx.chakra.simple_grid(
                            rx.foreach(
                                MarketplaceState.latest_listings,
                                listing_card,
                            ),
                            columns=[1, 2, 3],
                            spacing="6",
                            width="100%",
                        ),
                        rx.chakra.center(
                            rx.chakra.text(
                                "Nu există anunțuri momentan.",
                                color="gray.500",
                            ),
                            py="10",
                        ),
                    ),
                ),
                width="100%",
                py="10",
                spacing="6",
            ),
            max_width="container.xl",
        ),
    )


def features_section() -> rx.Component:
    """Secțiunea de caracteristici."""
    return rx.chakra.box(
        rx.chakra.container(
            rx.chakra.vstack(
                rx.chakra.heading(
                    "De ce să alegi Piata.ro?",
                    size="xl",
                    mb="8",
                ),
                rx.chakra.simple_grid(
                    rx.chakra.vstack(
                        rx.chakra.circle(
                            rx.chakra.icon("verified", size="xl", color="blue.500"),
                            size="16",
                            bg="blue.50",
                        ),
                        rx.chakra.heading("Utilizatori verificați", size="md", mb="2"),
                        rx.chakra.text(
                            "Toți utilizatorii sunt verificați pentru a asigura o comunitate de încredere.",
                            text_align="center",
                            color="gray.600",
                        ),
                        spacing="3",
                        p="6",
                        align="center",
                    ),
                    rx.chakra.vstack(
                        rx.chakra.circle(
                            rx.chakra.icon("shield", size="xl", color="blue.500"),
                            size="16",
                            bg="blue.50",
                        ),
                        rx.chakra.heading("Tranzacții sigure", size="md", mb="2"),
                        rx.chakra.text(
                            "Platforma noastră asigură tranzacții sigure și securizate.",
                            text_align="center",
                            color="gray.600",
                        ),
                        spacing="3",
                        p="6",
                        align="center",
                    ),
                    rx.chakra.vstack(
                        rx.chakra.circle(
                            rx.chakra.icon("bolt", size="xl", color="blue.500"),
                            size="16",
                            bg="blue.50",
                        ),
                        rx.chakra.heading("Rapid și ușor", size="md", mb="2"),
                        rx.chakra.text(
                            "Publicați anunțul în câteva minute și ajungeți la mii de cumpărători potențiali.",
                            text_align="center",
                            color="gray.600",
                        ),
                        spacing="3",
                        p="6",
                        align="center",
                    ),
                    columns=[1, 3],
                    spacing="6",
                ),
                width="100%",
                py="10",
                spacing="6",
            ),
            max_width="container.xl",
        ),
        bg="gray.50",
    )


def footer() -> rx.Component:
    """Subsolul paginii."""
    return rx.chakra.box(
        rx.chakra.container(
            rx.chakra.vstack(
                rx.chakra.simple_grid(
                    rx.chakra.vstack(
                        rx.chakra.heading("Piata.ro", size="md", mb="4", color="white"),
                        rx.chakra.text(
                            "Cel mai mare marketplace din România pentru cumpărare și vânzare.",
                            color="gray.400",
                        ),
                        rx.chakra.hstack(
                            rx.chakra.icon_button(
                                "facebook",
                                aria_label="Facebook",
                                variant="ghost",
                                color="white",
                                icon_size="lg",
                            ),
                            rx.chakra.icon_button(
                                "instagram",
                                aria_label="Instagram",
                                variant="ghost",
                                color="white",
                                icon_size="lg",
                            ),
                            rx.chakra.icon_button(
                                "twitter",
                                aria_label="Twitter",
                                variant="ghost",
                                color="white",
                                icon_size="lg",
                            ),
                            spacing="2",
                        ),
                        align_items="start",
                    ),
                    rx.chakra.vstack(
                        rx.chakra.heading("Linkuri rapide", size="md", mb="4", color="white"),
                        rx.chakra.link("Acasă", href="/", color="gray.400"),
                        rx.chakra.link("Anunțuri", href="/listings", color="gray.400"),
                        rx.chakra.link("Categorii", href="/categories", color="gray.400"),
                        rx.chakra.link("Adaugă anunț", href="/add-listing", color="gray.400"),
                        align_items="start",
                    ),
                    rx.chakra.vstack(
                        rx.chakra.heading("Informații", size="md", mb="4", color="white"),
                        rx.chakra.link("Despre noi", href="/about", color="gray.400"),
                        rx.chakra.link("Termeni și condiții", href="/terms", color="gray.400"),
                        rx.chakra.link("Politica de confidențialitate", href="/privacy", color="gray.400"),
                        rx.chakra.link("Contact", href="/contact", color="gray.400"),
                        align_items="start",
                    ),
                    rx.chakra.vstack(
                        rx.chakra.heading("Contact", size="md", mb="4", color="white"),
                        rx.chakra.text("Email: info@piata.ro", color="gray.400"),
                        rx.chakra.text("Telefon: +40 123 456 789", color="gray.400"),
                        rx.chakra.text("Adresă: Str. Exemplu nr. 123, București", color="gray.400"),
                        align_items="start",
                    ),
                    columns=[1, 2, 4],
                    spacing="8",
                ),
                rx.chakra.divider(my="6"),
                rx.chakra.text(
                    "© 2025 Piata.ro. Toate drepturile rezervate.",
                    color="gray.500",
                    text_align="center",
                ),
                width="100%",
                py="10",
                spacing="6",
            ),
            max_width="container.xl",
        ),
        bg="gray.900",
    )


def index() -> rx.Component:
    """Pagina principală."""
    return rx.chakra.box(
        navbar(),
        hero_section(),
        featured_listings_section(),
        categories_section(),
        latest_listings_section(),
        features_section(),
        footer(),
        on_mount=MarketplaceState.fetch_data,
    )


# Creează aplicația
app = rx.App()
app.add_page(index)
