"""Pagina pentru adăugarea unui anunț nou."""

import reflex as rx
from typing import List, Dict, Any, Optional
from datetime import datetime

from frontend_reflex.components.navbar import navbar
from frontend_reflex.components.footer import footer
from frontend_reflex.components.credits_panel import credits_panel
from frontend_reflex.state import State


class AddListingState(State):
    """Starea pentru pagina de adăugare anunț."""

    # Datele anunțului
    title: str = ""
    description: str = ""
    price: str = ""
    currency: str = "RON"
    location: str = ""
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    images: List[str] = []

    # Opțiuni de promovare
    listing_type: str = "standard"  # standard, promoted, premium, vip
    duration: int = 7  # zile

    # Costul în credite
    cost: int = 1

    # Categorii disponibile
    categories: List[Dict[str, Any]] = []
    subcategories: List[Dict[str, Any]] = []

    # Stare formular
    form_error: Optional[str] = None
    form_success: Optional[str] = None

    def compute_cost(self):
        """Calculează costul în credite pentru anunț."""
        costs = {
            "standard": {7: 1, 14: 2, 30: 3},
            "promoted": {3: 3, 7: 5, 14: 8},
            "premium": {7: 5, 14: 9, 30: 15},
            "vip": {7: 7, 14: 10, 30: 20},
        }

        self.cost = costs.get(self.listing_type, {}).get(self.duration, 1)

    def set_listing_type(self, listing_type: str):
        """Setează tipul anunțului."""
        self.listing_type = listing_type
        self.compute_cost()

    def set_duration(self, duration: int):
        """Setează durata anunțului."""
        self.duration = duration
        self.compute_cost()

    def set_title(self, title: str):
        """Setează titlul anunțului."""
        self.title = title

    def set_description(self, description: str):
        """Setează descrierea anunțului."""
        self.description = description

    def set_price(self, price: str):
        """Setează prețul anunțului."""
        self.price = price

    def set_currency(self, currency: str):
        """Setează moneda anunțului."""
        self.currency = currency

    def set_location(self, location: str):
        """Setează locația anunțului."""
        self.location = location

    def set_category(self, category_id: int):
        """Setează categoria și încarcă subcategoriile."""
        self.category_id = category_id
        self.subcategory_id = None

        # În producție, se vor încărca subcategoriile de la API
        # Simulare pentru dezvoltare
        self.subcategories = [
            {"id": 101, "name": "Subcategorie 1", "parent_id": category_id},
            {"id": 102, "name": "Subcategorie 2", "parent_id": category_id},
            {"id": 103, "name": "Subcategorie 3", "parent_id": category_id},
        ]

    def set_subcategory_id(self, subcategory_id: int):
        """Setează subcategoria anunțului."""
        self.subcategory_id = subcategory_id

    async def fetch_categories(self):
        """Încarcă categoriile disponibile."""
        self.is_loading = True

        # În producție, se vor încărca categoriile de la API
        # Simulare pentru dezvoltare
        self.categories = [
            {"id": 1, "name": "Imobiliare"},
            {"id": 2, "name": "Auto"},
            {"id": 3, "name": "Electronice"},
            {"id": 4, "name": "Servicii"},
            {"id": 5, "name": "Locuri de muncă"},
            {"id": 6, "name": "Modă"},
        ]

        self.is_loading = False

    async def submit_listing(self, form_data: Dict[str, Any]):
        """Trimite anunțul către server."""
        self.is_loading = True
        self.form_error = None
        self.form_success = None

        # Validare date
        if not self.title or not self.description or not self.location:
            self.form_error = "Te rugăm să completezi toate câmpurile obligatorii."
            self.is_loading = False
            return

        if not self.category_id:
            self.form_error = "Te rugăm să selectezi o categorie."
            self.is_loading = False
            return

        # Verifică dacă utilizatorul are suficiente credite
        if self.credits < self.cost:
            self.form_error = f"Nu ai suficiente credite. Ai nevoie de {self.cost} credite pentru acest anunț."
            self.is_loading = False
            return

        try:
            # În producție, se va trimite anunțul către API-ul Django
            # Simulare pentru dezvoltare

            # Scade creditele
            self.credits -= self.cost

            # Simulează un răspuns de succes
            self.form_success = "Anunțul tău a fost publicat cu succes!"

            # Resetează formularul
            self.title = ""
            self.description = ""
            self.price = ""
            self.location = ""
            self.category_id = None
            self.subcategory_id = None
            self.images = []
            self.listing_type = "standard"
            self.duration = 7
            self.compute_cost()

        except Exception as e:
            self.form_error = f"Eroare la publicarea anunțului: {str(e)}"

        self.is_loading = False


def add_listing() -> rx.Component:
    """Pagina pentru adăugarea unui anunț nou."""
    return rx.box(
        navbar(),

        rx.box(
            rx.vstack(
                rx.heading("Adaugă un anunț nou", size="xl", mb="6"),

                # Afișare erori/succes
                rx.cond(
                    AddListingState.form_error,
                    rx.alert(
                        rx.alert_icon(),
                        rx.alert_title(AddListingState.form_error),
                        status="error",
                        mb="4",
                    ),
                ),
                rx.cond(
                    AddListingState.form_success,
                    rx.alert(
                        rx.alert_icon(),
                        rx.alert_title(AddListingState.form_success),
                        status="success",
                        mb="4",
                    ),
                ),

                # Formular și panou credite
                rx.hstack(
                    # Formular anunț
                    rx.form(
                        rx.vstack(
                            rx.heading("Informații anunț", size="md", mb="4"),

                            # Titlu
                            rx.form_control(
                                rx.form_label("Titlu", html_for="title"),
                                rx.input(
                                    id="title",
                                    placeholder="Titlul anunțului",
                                    value=AddListingState.title,
                                    on_change=AddListingState.set_title,
                                    required=True,
                                ),
                                is_required=True,
                            ),

                            # Descriere
                            rx.form_control(
                                rx.form_label("Descriere", html_for="description"),
                                rx.text_area(
                                    id="description",
                                    placeholder="Descrierea detaliată a anunțului",
                                    value=AddListingState.description,
                                    on_change=AddListingState.set_description,
                                    required=True,
                                    min_height="150px",
                                ),
                                is_required=True,
                            ),

                            # Preț și monedă
                            rx.hstack(
                                rx.form_control(
                                    rx.form_label("Preț", html_for="price"),
                                    rx.input(
                                        id="price",
                                        type_="number",
                                        placeholder="Preț",
                                        value=AddListingState.price,
                                        on_change=AddListingState.set_price,
                                    ),
                                    width="70%",
                                ),
                                rx.form_control(
                                    rx.form_label("Monedă", html_for="currency"),
                                    rx.select(
                                        ["RON", "EUR", "USD"],
                                        id="currency",
                                        value=AddListingState.currency,
                                        on_change=AddListingState.set_currency,
                                    ),
                                    width="30%",
                                ),
                                width="100%",
                            ),

                            # Locație
                            rx.form_control(
                                rx.form_label("Locație", html_for="location"),
                                rx.input(
                                    id="location",
                                    placeholder="Orașul sau localitatea",
                                    value=AddListingState.location,
                                    on_change=AddListingState.set_location,
                                    required=True,
                                ),
                                is_required=True,
                            ),

                            # Categorie și subcategorie
                            rx.hstack(
                                rx.form_control(
                                    rx.form_label("Categorie", html_for="category"),
                                    rx.select(
                                        rx.foreach(
                                            AddListingState.categories,
                                            lambda cat: rx.option(cat["name"], value=cat["id"]),
                                        ),
                                        id="category",
                                        placeholder="Selectează categoria",
                                        value=AddListingState.category_id,
                                        on_change=AddListingState.set_category,
                                        required=True,
                                    ),
                                    is_required=True,
                                    width="50%",
                                ),
                                rx.form_control(
                                    rx.form_label("Subcategorie", html_for="subcategory"),
                                    rx.select(
                                        rx.foreach(
                                            AddListingState.subcategories,
                                            lambda subcat: rx.option(subcat["name"], value=subcat["id"]),
                                        ),
                                        id="subcategory",
                                        placeholder="Selectează subcategoria",
                                        value=AddListingState.subcategory_id,
                                        on_change=AddListingState.set_subcategory_id,
                                        is_disabled=AddListingState.category_id is None,
                                    ),
                                    width="50%",
                                ),
                                width="100%",
                            ),

                            # Încărcare imagini
                            rx.form_control(
                                rx.form_label("Imagini", html_for="images"),
                                rx.file_upload(
                                    rx.file_upload_button("Încarcă imagini"),
                                    rx.file_upload_drop_zone("Trage și plasează imaginile aici"),
                                    rx.file_upload_preview(),
                                    id="images",
                                    multiple=True,
                                    accept="image/*",
                                    max_files=10,
                                ),
                            ),

                            # Opțiuni de promovare
                            rx.heading("Opțiuni de promovare", size="md", mt="6", mb="4"),

                            # Tip anunț
                            rx.form_control(
                                rx.form_label("Tip anunț", html_for="listing_type"),
                                rx.radio_group(
                                    rx.hstack(
                                        rx.radio(
                                            rx.vstack(
                                                rx.text("Standard", font_weight="bold"),
                                                rx.text("Vizibilitate normală", font_size="xs"),
                                                align_items="start",
                                            ),
                                            value="standard",
                                        ),
                                        rx.radio(
                                            rx.vstack(
                                                rx.text("Promovat", font_weight="bold", color="blue.500"),
                                                rx.text("Afișat în secțiunea de anunțuri promovate", font_size="xs"),
                                                align_items="start",
                                            ),
                                            value="promoted",
                                        ),
                                        rx.radio(
                                            rx.vstack(
                                                rx.text("Premium", font_weight="bold", color="purple.500"),
                                                rx.text("Afișat în partea de sus a listei", font_size="xs"),
                                                align_items="start",
                                            ),
                                            value="premium",
                                        ),
                                        rx.radio(
                                            rx.vstack(
                                                rx.text("VIP", font_weight="bold", color="orange.500"),
                                                rx.text("Afișat în partea de sus + evidențiat", font_size="xs"),
                                                align_items="start",
                                            ),
                                            value="vip",
                                        ),
                                        spacing="4",
                                        wrap="wrap",
                                    ),
                                    id="listing_type",
                                    value=AddListingState.listing_type,
                                    on_change=AddListingState.set_listing_type,
                                ),
                            ),

                            # Durată anunț
                            rx.form_control(
                                rx.form_label("Durată anunț", html_for="duration"),
                                rx.radio_group(
                                    rx.hstack(
                                        rx.radio("7 zile", value=7),
                                        rx.radio("14 zile", value=14),
                                        rx.radio("30 zile", value=30),
                                        spacing="6",
                                    ),
                                    id="duration",
                                    value=AddListingState.duration,
                                    on_change=AddListingState.set_duration,
                                ),
                            ),

                            # Cost total
                            rx.hstack(
                                rx.text("Cost total:"),
                                rx.text(
                                    f"{AddListingState.cost} credite",
                                    font_weight="bold",
                                    color="blue.500",
                                ),
                                bg="blue.50",
                                p="3",
                                border_radius="md",
                                width="100%",
                                justify="center",
                                mt="4",
                            ),

                            # Buton publicare
                            rx.button(
                                "Publică anunțul",
                                type_="submit",
                                width="100%",
                                color_scheme="blue",
                                size="lg",
                                mt="6",
                                is_loading=AddListingState.is_loading,
                            ),

                            width="100%",
                            spacing="4",
                            align_items="start",
                        ),
                        on_submit=AddListingState.submit_listing,
                        width="65%",
                    ),

                    # Panou credite
                    rx.box(
                        credits_panel(),
                        width="35%",
                    ),

                    align_items="start",
                    spacing="6",
                    width="100%",
                ),

                max_width="1200px",
                width="100%",
                spacing="6",
                py="10",
            ),
            mx="auto",
            px="4",
        ),

        footer(),

        on_mount=AddListingState.fetch_categories,
    )
