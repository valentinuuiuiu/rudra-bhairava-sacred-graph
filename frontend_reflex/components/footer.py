"""Componenta de subsol pentru Piata.ro."""

import reflex as rx


def footer() -> rx.Component:
    """Subsolul pentru Piata.ro."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Piata.ro", size="md", mb="2"),
                    rx.text(
                        "Cel mai bun marketplace pentru cumpărare și vânzare în România."
                    ),
                    align_items="start",
                ),
                rx.vstack(
                    rx.heading("Linkuri rapide", size="md", mb="2"),
                    rx.link("Acasă", href="/"),
                    rx.link("Anunțuri", href="/listings"),
                    rx.link("Categorii", href="/categories"),
                    rx.link("Adaugă anunț", href="/add-listing"),
                    align_items="start",
                ),
                rx.vstack(
                    rx.heading("Informații", size="md", mb="2"),
                    rx.link("Despre noi", href="/about"),
                    rx.link("Termeni și condiții", href="/terms"),
                    rx.link("Politica de confidențialitate", href="/privacy"),
                    rx.link("Contact", href="/contact"),
                    align_items="start",
                ),
                rx.vstack(
                    rx.heading("Contact", size="md", mb="2"),
                    rx.text("Email: info@piata.ro"),
                    rx.text("Telefon: +40 123 456 789"),
                    rx.text("Adresă: Str. Exemplu nr. 123, București"),
                    align_items="start",
                ),
                justify="space-between",
                width="100%",
                spacing="8",
                wrap="wrap",
            ),
            rx.divider(),
            rx.text("© 2025 Piata.ro. Toate drepturile rezervate."),
            width="100%",
            max_width="1200px",
            mx="auto",
            py="10",
            px="4",
            spacing="8",
        ),
        bg="gray.800",
        color="white",
        width="100%",
    )
