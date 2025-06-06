"""Componenta card categorie pentru Piata.ro."""

import reflex as rx
from typing import Optional


# Mapare categorii la icoane și culori
CATEGORY_ICONS = {
    "Imobiliare": ("home", "#28a745"),
    "Auto moto": ("car", "#007bff"),
    "Locuri de muncă": ("briefcase", "#fd7e14"),
    "Matrimoniale": ("heart", "#e83e8c"),
    "Servicii": ("tools", "#dc3545"),
    "Electronice": ("laptop", "#6f42c1"),
    "Modă și accesorii": ("tshirt", "#6610f2"),
    "Animale": ("paw", "#fd7e14"),
    "Casă și grădină": ("home", "#20c997"),
    "Timp liber și sport": ("futbol", "#17a2b8"),
    "Mamă și copil": ("baby", "#ffc107"),
    "Cazare turism": ("suitcase", "#20c997"),
    # Default pentru alte categorii
    "default": ("tag", "#0275d8"),
}


def get_category_icon_and_color(name: str) -> tuple:
    """Returnează iconița și culoarea pentru o categorie."""
    return CATEGORY_ICONS.get(name, CATEGORY_ICONS["default"])


def category_card(
    id: int,
    name: str,
    icon: Optional[str] = None,
    color: Optional[str] = None,
) -> rx.Component:
    """Card pentru afișarea unei categorii în stil publi24.ro."""
    # Obține iconița și culoarea dacă nu sunt furnizate
    if not icon or not color:
        icon, color = get_category_icon_and_color(name)

    return rx.link(
        rx.vstack(
            rx.center(
                rx.icon(
                    icon,
                    size="xl",
                    color="white",
                ),
                bg=color,
                width="70px",
                height="70px",
                border_radius="full",
                mb="3",
            ),
            rx.text(
                name,
                font_weight="600",
                color="gray.700",
                text_align="center",
            ),
            align="center",
            spacing="2",
            _hover={"transform": "translateY(-5px)"},
            transition="all 0.2s",
            py="2",
        ),
        href=f"/category/{id}",
        _hover={"text_decoration": "none"},
        width="120px",
        height="100%",
    )
