"""Componenta pentru afișarea și gestionarea creditelor."""

import reflex as rx
from frontend_reflex.state import State


def credits_panel() -> rx.Component:
    """Panou pentru afișarea și gestionarea creditelor utilizatorului."""
    return rx.cond(
        State.is_authenticated,
        rx.box(
            rx.vstack(
                # Titlu
                rx.heading("Credite și Abonament", size="md", mb="4"),
                
                # Afișare credite curente
                rx.hstack(
                    rx.icon("coin", color="yellow.500"),
                    rx.text("Credite disponibile:"),
                    rx.text(
                        State.credits,
                        font_weight="bold",
                        color="blue.500",
                    ),
                    spacing="2",
                    mb="3",
                ),
                
                # Afișare abonament
                rx.cond(
                    State.subscription_type,
                    rx.vstack(
                        rx.hstack(
                            rx.icon("star", color="purple.500"),
                            rx.text("Abonament:"),
                            rx.text(
                                State.subscription_type,
                                font_weight="bold",
                                color="purple.500",
                            ),
                            spacing="2",
                        ),
                        rx.text(
                            f"Expiră la: {State.subscription_expires.strftime('%d.%m.%Y') if State.subscription_expires else 'N/A'}",
                            font_size="sm",
                            color="gray.500",
                        ),
                        align_items="start",
                        mb="4",
                    ),
                    rx.text("Nu ai un abonament activ.", mb="4", color="gray.500"),
                ),
                
                # Butoane pentru cumpărare credite
                rx.heading("Cumpără credite", size="sm", mb="2"),
                rx.hstack(
                    rx.button(
                        "10 credite",
                        on_click=lambda: State.buy_credits(10, "card"),
                        size="sm",
                    ),
                    rx.button(
                        "50 credite",
                        on_click=lambda: State.buy_credits(50, "card"),
                        size="sm",
                    ),
                    rx.button(
                        "100 credite",
                        on_click=lambda: State.buy_credits(100, "card"),
                        size="sm",
                    ),
                    spacing="2",
                    wrap="wrap",
                    mb="4",
                ),
                
                # Butoane pentru abonamente
                rx.heading("Abonamente", size="sm", mb="2"),
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Basic", size="xs"),
                            rx.text("10 credite/lună", font_size="xs"),
                            rx.text("5 EUR/lună", font_weight="bold"),
                            rx.button(
                                "Activează",
                                on_click=lambda: State.upgrade_subscription("basic"),
                                size="xs",
                                variant="outline",
                            ),
                            p="3",
                            border="1px solid",
                            border_color="gray.200",
                            border_radius="md",
                            align_items="center",
                        ),
                        rx.vstack(
                            rx.heading("Premium", size="xs"),
                            rx.text("50 credite/lună", font_size="xs"),
                            rx.text("20 EUR/lună", font_weight="bold"),
                            rx.button(
                                "Activează",
                                on_click=lambda: State.upgrade_subscription("premium"),
                                size="xs",
                                variant="outline",
                                color_scheme="purple",
                            ),
                            p="3",
                            border="1px solid",
                            border_color="purple.200",
                            border_radius="md",
                            align_items="center",
                            bg="purple.50",
                        ),
                        rx.vstack(
                            rx.heading("Business", size="xs"),
                            rx.text("200 credite/lună", font_size="xs"),
                            rx.text("50 EUR/lună", font_weight="bold"),
                            rx.button(
                                "Activează",
                                on_click=lambda: State.upgrade_subscription("business"),
                                size="xs",
                                variant="outline",
                                color_scheme="orange",
                            ),
                            p="3",
                            border="1px solid",
                            border_color="orange.200",
                            border_radius="md",
                            align_items="center",
                            bg="orange.50",
                        ),
                        spacing="2",
                        wrap="wrap",
                    ),
                    align_items="stretch",
                    width="100%",
                ),
                
                # Informații despre utilizarea creditelor
                rx.box(
                    rx.text(
                        "Cum se folosesc creditele:",
                        font_weight="bold",
                        mb="2",
                    ),
                    rx.unordered_list(
                        rx.list_item("1 credit - Anunț standard pentru 7 zile"),
                        rx.list_item("3 credite - Anunț promovat pentru 3 zile"),
                        rx.list_item("5 credite - Anunț premium pentru 7 zile"),
                        rx.list_item("10 credite - Anunț VIP pentru 14 zile"),
                        spacing="1",
                        pl="4",
                    ),
                    mt="4",
                    p="3",
                    bg="blue.50",
                    border_radius="md",
                    font_size="sm",
                ),
                
                width="100%",
                align_items="start",
                spacing="3",
            ),
            p="4",
            border="1px solid",
            border_color="gray.200",
            border_radius="md",
            bg="white",
            width="100%",
        ),
        rx.box(
            rx.alert(
                rx.alert_icon(),
                rx.alert_title("Trebuie să fii autentificat pentru a vedea creditele."),
                status="warning",
            ),
            width="100%",
        ),
    )
