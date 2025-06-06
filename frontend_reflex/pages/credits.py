"""Pagina pentru gestionarea creditelor."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import reflex as rx

from frontend_reflex.components.footer import footer
from frontend_reflex.components.navbar import navbar
from frontend_reflex.state import State


class CreditsState(State):
    """Starea pentru pagina de credite."""

    # Istoricul tranzacțiilor
    transactions: List[Dict[str, Any]] = []

    # Metoda de plată selectată
    payment_method: str = "card"

    # Suma personalizată
    custom_amount: int = 0

    # Stare formular
    payment_error: Optional[str] = None
    payment_success: Optional[str] = None

    async def fetch_transactions(self):
        """Încarcă istoricul tranzacțiilor."""
        self.is_loading = True

        # În producție, se vor încărca tranzacțiile de la API
        # Simulare pentru dezvoltare
        self.transactions = [
            {
                "id": 1,
                "type": "purchase",
                "amount": 10,
                "credits": 10,
                "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "status": "completed",
                "payment_method": "card",
            },
            {
                "id": 2,
                "type": "subscription",
                "amount": 20,
                "credits": 50,
                "date": (datetime.now() - timedelta(days=15)).strftime(
                    "%d.%m.%Y %H:%M"
                ),
                "status": "completed",
                "payment_method": "paypal",
            },
            {
                "id": 3,
                "type": "usage",
                "amount": 0,
                "credits": -3,
                "date": (datetime.now() - timedelta(days=5)).strftime("%d.%m.%Y %H:%M"),
                "status": "completed",
                "description": "Anunț promovat: Apartament de vânzare",
            },
        ]

        self.is_loading = False

    def set_payment_method(self, method: str):
        """Setează metoda de plată."""
        self.payment_method = method

    def set_custom_amount(self, amount: str):
        """Setează suma personalizată."""
        try:
            self.custom_amount = int(amount)
        except ValueError:
            self.custom_amount = 0

    async def purchase_credits(self, amount: int):
        """Cumpără credite."""
        self.is_loading = True
        self.payment_error = None
        self.payment_success = None

        if amount <= 0:
            self.payment_error = "Suma trebuie să fie mai mare decât zero."
            self.is_loading = False
            return

        try:
            # În producție, se va conecta la API-ul Django pentru procesarea plății
            # Simulare pentru dezvoltare
            self.credits += amount

            # Adaugă tranzacția în istoric
            self.transactions.insert(
                0,
                {
                    "id": len(self.transactions) + 1,
                    "type": "purchase",
                    "amount": amount * 0.5,  # Preț în EUR (0.5 EUR per credit)
                    "credits": amount,
                    "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "status": "completed",
                    "payment_method": self.payment_method,
                },
            )

            self.payment_success = f"Ai cumpărat cu succes {amount} credite!"
            self.custom_amount = 0
        except Exception as e:
            self.payment_error = f"Eroare la procesarea plății: {str(e)}"

        self.is_loading = False


def credits() -> rx.Component:
    """Pagina pentru gestionarea creditelor."""
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.heading("Credite și Abonamente", size="xl", mb="6"),
                # Afișare erori/succes
                rx.cond(
                    CreditsState.payment_error,
                    rx.alert(
                        rx.alert_icon(),
                        rx.alert_title(CreditsState.payment_error),
                        status="error",
                        mb="4",
                    ),
                ),
                rx.cond(
                    CreditsState.payment_success,
                    rx.alert(
                        rx.alert_icon(),
                        rx.alert_title(CreditsState.payment_success),
                        status="success",
                        mb="4",
                    ),
                ),
                # Informații credite și abonament
                rx.hstack(
                    # Credite
                    rx.stat(
                        rx.stat_label("Credite disponibile"),
                        rx.stat_number(CreditsState.credits),
                        rx.stat_help_text(
                            rx.icon("info"),
                            rx.text(
                                "Folosește creditele pentru a promova anunțurile tale"
                            ),
                            spacing="1",
                        ),
                        p="6",
                        border="1px solid",
                        border_color="blue.200",
                        border_radius="lg",
                        bg="blue.50",
                    ),
                    # Abonament
                    rx.stat(
                        rx.stat_label("Abonament curent"),
                        rx.stat_number(
                            CreditsState.subscription_type or "Fără abonament"
                        ),
                        rx.stat_help_text(
                            rx.cond(
                                CreditsState.subscription_expires,
                                rx.hstack(
                                    rx.icon("time"),
                                    rx.text(
                                        f"Expiră la: {CreditsState.subscription_expires.strftime('%d.%m.%Y') if CreditsState.subscription_expires else 'N/A'}"
                                    ),
                                    spacing="1",
                                ),
                                rx.text("Abonează-te pentru a primi credite lunar"),
                            ),
                        ),
                        p="6",
                        border="1px solid",
                        border_color="purple.200",
                        border_radius="lg",
                        bg="purple.50",
                    ),
                    spacing="6",
                    width="100%",
                ),
                # Cumpără credite
                rx.box(
                    rx.vstack(
                        rx.heading("Cumpără credite", size="lg", mb="4"),
                        # Pachete de credite
                        rx.hstack(
                            rx.vstack(
                                rx.heading("10 credite", size="md"),
                                rx.text("5 EUR", font_weight="bold", font_size="xl"),
                                rx.button(
                                    "Cumpără",
                                    on_click=lambda: CreditsState.purchase_credits(10),
                                    color_scheme="blue",
                                ),
                                p="6",
                                border="1px solid",
                                border_color="gray.200",
                                border_radius="md",
                                align_items="center",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.heading("50 credite", size="md"),
                                rx.text("20 EUR", font_weight="bold", font_size="xl"),
                                rx.text(
                                    "Economisești 5 EUR",
                                    color="green.500",
                                    font_size="sm",
                                ),
                                rx.button(
                                    "Cumpără",
                                    on_click=lambda: CreditsState.purchase_credits(50),
                                    color_scheme="blue",
                                ),
                                p="6",
                                border="1px solid",
                                border_color="blue.200",
                                border_radius="md",
                                align_items="center",
                                bg="blue.50",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.heading("100 credite", size="md"),
                                rx.text("35 EUR", font_weight="bold", font_size="xl"),
                                rx.text(
                                    "Economisești 15 EUR",
                                    color="green.500",
                                    font_size="sm",
                                ),
                                rx.button(
                                    "Cumpără",
                                    on_click=lambda: CreditsState.purchase_credits(100),
                                    color_scheme="blue",
                                ),
                                p="6",
                                border="1px solid",
                                border_color="gray.200",
                                border_radius="md",
                                align_items="center",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.heading("Sumă personalizată", size="md"),
                                rx.hstack(
                                    rx.number_input(
                                        value=CreditsState.custom_amount,
                                        on_change=CreditsState.set_custom_amount,
                                        min_=1,
                                        max_=1000,
                                    ),
                                    rx.text("credite"),
                                ),
                                rx.text(
                                    f"{CreditsState.custom_amount * 0.5} EUR",
                                    font_weight="bold",
                                ),
                                rx.button(
                                    "Cumpără",
                                    on_click=lambda: CreditsState.purchase_credits(
                                        CreditsState.custom_amount
                                    ),
                                    color_scheme="blue",
                                    is_disabled=CreditsState.custom_amount <= 0,
                                ),
                                p="6",
                                border="1px solid",
                                border_color="gray.200",
                                border_radius="md",
                                align_items="center",
                                width="100%",
                            ),
                            spacing="4",
                            width="100%",
                            wrap="wrap",
                        ),
                        # Metode de plată
                        rx.form_control(
                            rx.form_label("Metodă de plată"),
                            rx.radio_group(
                                rx.hstack(
                                    rx.radio(
                                        rx.hstack(
                                            rx.icon("credit-card"),
                                            rx.text("Card bancar"),
                                            spacing="2",
                                        ),
                                        value="card",
                                    ),
                                    rx.radio(
                                        rx.hstack(
                                            rx.icon("paypal"),
                                            rx.text("PayPal"),
                                            spacing="2",
                                        ),
                                        value="paypal",
                                    ),
                                    rx.radio(
                                        rx.hstack(
                                            rx.icon("bank"),
                                            rx.text("Transfer bancar"),
                                            spacing="2",
                                        ),
                                        value="bank",
                                    ),
                                    spacing="6",
                                ),
                                value=CreditsState.payment_method,
                                on_change=CreditsState.set_payment_method,
                            ),
                            mt="4",
                        ),
                        width="100%",
                        align_items="start",
                        spacing="4",
                    ),
                    p="6",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="lg",
                    bg="white",
                    width="100%",
                    mt="6",
                ),
                # Abonamente
                rx.box(
                    rx.vstack(
                        rx.heading("Abonamente", size="lg", mb="4"),
                        rx.hstack(
                            rx.vstack(
                                rx.heading("Basic", size="md"),
                                rx.text("10 credite/lună", mb="2"),
                                rx.text(
                                    "5 EUR/lună", font_weight="bold", font_size="xl"
                                ),
                                rx.button(
                                    "Abonează-te",
                                    on_click=lambda: CreditsState.upgrade_subscription(
                                        "basic"
                                    ),
                                    variant="outline",
                                ),
                                p="6",
                                border="1px solid",
                                border_color="gray.200",
                                border_radius="md",
                                align_items="center",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.heading("Premium", size="md"),
                                rx.text("50 credite/lună", mb="2"),
                                rx.text(
                                    "20 EUR/lună", font_weight="bold", font_size="xl"
                                ),
                                rx.badge("Popular", color_scheme="purple", mb="2"),
                                rx.button(
                                    "Abonează-te",
                                    on_click=lambda: CreditsState.upgrade_subscription(
                                        "premium"
                                    ),
                                    color_scheme="purple",
                                ),
                                p="6",
                                border="1px solid",
                                border_color="purple.200",
                                border_radius="md",
                                align_items="center",
                                bg="purple.50",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.heading("Business", size="md"),
                                rx.text("200 credite/lună", mb="2"),
                                rx.text(
                                    "50 EUR/lună", font_weight="bold", font_size="xl"
                                ),
                                rx.button(
                                    "Abonează-te",
                                    on_click=lambda: CreditsState.upgrade_subscription(
                                        "business"
                                    ),
                                    variant="outline",
                                    color_scheme="orange",
                                ),
                                p="6",
                                border="1px solid",
                                border_color="orange.200",
                                border_radius="md",
                                align_items="center",
                                width="100%",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        width="100%",
                        align_items="start",
                        spacing="4",
                    ),
                    p="6",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="lg",
                    bg="white",
                    width="100%",
                    mt="6",
                ),
                # Istoricul tranzacțiilor
                rx.box(
                    rx.vstack(
                        rx.heading("Istoricul tranzacțiilor", size="lg", mb="4"),
                        rx.cond(
                            CreditsState.is_loading,
                            rx.center(rx.spinner(size="xl"), width="100%", py="10"),
                            rx.cond(
                                len(CreditsState.transactions) > 0,
                                rx.table(
                                    rx.thead(
                                        rx.tr(
                                            rx.th("Data"),
                                            rx.th("Tip"),
                                            rx.th("Credite"),
                                            rx.th("Sumă"),
                                            rx.th("Metodă"),
                                            rx.th("Status"),
                                        ),
                                    ),
                                    rx.tbody(
                                        rx.foreach(
                                            CreditsState.transactions,
                                            lambda tx: rx.tr(
                                                rx.td(tx["date"]),
                                                rx.td(
                                                    rx.badge(
                                                        {
                                                            "purchase": "Cumpărare",
                                                            "subscription": "Abonament",
                                                            "usage": "Utilizare",
                                                        }.get(tx["type"], tx["type"]),
                                                        color_scheme={
                                                            "purchase": "green",
                                                            "subscription": "purple",
                                                            "usage": "blue",
                                                        }.get(tx["type"], "gray"),
                                                    ),
                                                ),
                                                rx.td(
                                                    (
                                                        f"+{tx['credits']}"
                                                        if tx["credits"] > 0
                                                        else tx["credits"]
                                                    ),
                                                    color=(
                                                        "green.500"
                                                        if tx["credits"] > 0
                                                        else "red.500"
                                                    ),
                                                    font_weight="bold",
                                                ),
                                                rx.td(
                                                    (
                                                        f"{tx['amount']} EUR"
                                                        if tx["amount"] > 0
                                                        else "-"
                                                    ),
                                                ),
                                                rx.td(tx.get("payment_method", "-")),
                                                rx.td(
                                                    rx.badge(
                                                        {
                                                            "completed": "Finalizat",
                                                            "pending": "În așteptare",
                                                            "failed": "Eșuat",
                                                        }.get(
                                                            tx["status"], tx["status"]
                                                        ),
                                                        color_scheme={
                                                            "completed": "green",
                                                            "pending": "yellow",
                                                            "failed": "red",
                                                        }.get(tx["status"], "gray"),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                    width="100%",
                                ),
                                rx.center(
                                    rx.text("Nu există tranzacții în istoric."),
                                    width="100%",
                                    py="10",
                                ),
                            ),
                        ),
                        width="100%",
                        align_items="start",
                        spacing="4",
                    ),
                    p="6",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="lg",
                    bg="white",
                    width="100%",
                    mt="6",
                    overflow_x="auto",
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
        on_mount=CreditsState.fetch_transactions,
    )
