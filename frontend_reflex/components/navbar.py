"""Componenta de navigare pentru Piata.ro."""

import reflex as rx
from frontend_reflex.state import State


def navbar() -> rx.Component:
    """Bara de navigare pentru Piata.ro."""
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(src="/favicon.ico", width="30px", height="30px"),
                rx.heading("Piata.ro", size="md"),
                spacing="2",
                as_="a",
                href="/",
                _hover={"text_decoration": "none"},
            ),
            rx.spacer(),
            rx.hstack(
                rx.menu(
                    rx.menu_button(
                        "Categorii",
                        right_icon=rx.icon("chevron_down"),
                    ),
                    rx.menu_list(
                        rx.menu_item("Electronice", as_="a", href="/category/1"),
                        rx.menu_item("Vehicule", as_="a", href="/category/2"),
                        rx.menu_item("Imobiliare", as_="a", href="/category/3"),
                        rx.menu_item("Locuri de muncă", as_="a", href="/category/4"),
                        rx.menu_item("Servicii", as_="a", href="/category/5"),
                        rx.menu_item("Modă", as_="a", href="/category/6"),
                        rx.menu_item("Casă și grădină", as_="a", href="/category/7"),
                        rx.menu_item("Sport și timp liber", as_="a", href="/category/8"),
                    ),
                ),
                rx.link("Anunțuri", href="/listings"),
                rx.link("Despre noi", href="/about"),
                rx.link("Contact", href="/contact"),
                spacing="6",
            ),
            rx.spacer(),
            rx.cond(
                State.is_authenticated,
                rx.hstack(
                    rx.menu(
                        rx.menu_button(
                            rx.hstack(
                                rx.avatar(size="sm"),
                                rx.text(State.username),
                                spacing="2",
                            ),
                        ),
                        rx.menu_list(
                            rx.menu_item("Profilul meu", as_="a", href="/profile"),
                            rx.menu_item("Anunțurile mele", as_="a", href="/my-listings"),
                            rx.menu_item("Favorite", as_="a", href="/favorites"),
                            rx.menu_item("Mesaje", as_="a", href="/messages"),
                            rx.menu_item(
                                rx.hstack(
                                    rx.icon("coin", color="yellow.500"),
                                    rx.text(f"Credite: {State.credits}"),
                                    spacing="1",
                                ),
                                as_="a",
                                href="/credits"
                            ),
                            rx.menu_divider(),
                            rx.menu_item("Deconectare", on_click=State.logout),
                        ),
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("add"),
                            rx.text("Adaugă anunț"),
                            spacing="1",
                        ),
                        color_scheme="orange",
                        as_="a",
                        href="/add-listing",
                    ),
                    spacing="4",
                ),
                rx.hstack(
                    rx.button("Autentificare", variant="ghost", as_="a", href="/login"),
                    rx.button("Înregistrare", color_scheme="blue", as_="a", href="/register"),
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
