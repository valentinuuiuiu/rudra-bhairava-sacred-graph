"""Piata.ro - O aplicație de marketplace construită cu Reflex și Django."""

import reflex as rx
from rxconfig import config

# Definim o pagină simplă pentru a testa aplicația
def index():
    return rx.center(
        rx.vstack(
            rx.heading("Piata.ro", size="2xl"),
            rx.text("Bine ați venit la Piata.ro - Marketplace-ul românesc"),
            rx.button("Explorează anunțuri", color_scheme="blue", size="lg"),
            spacing="4",
            padding="10",
        ),
        height="100vh",
    )

# Creează aplicația
app = rx.App()

# Adaugă pagina la aplicație
app.add_page(index, route="/")

# Configurează tema
app.theme = rx.theme(
    colors={
        "primary": {
            "50": "#e6f1ff",
            "100": "#cce3ff",
            "200": "#99c7ff",
            "300": "#66abff",
            "400": "#338fff",
            "500": "#0073ff",
            "600": "#005ccc",
            "700": "#004599",
            "800": "#002e66",
            "900": "#001733",
        },
    },
    fonts={
        "heading": "Roboto, sans-serif",
        "body": "Roboto, sans-serif",
    },
)
