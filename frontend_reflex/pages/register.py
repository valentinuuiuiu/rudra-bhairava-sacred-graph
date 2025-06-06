"""Pagina de înregistrare pentru aplicația de marketplace Piata.ro."""

import reflex as rx

from frontend_reflex.components.footer import footer
from frontend_reflex.components.navbar import navbar
from frontend_reflex.state import State


class RegisterState(State):
    """Starea pentru pagina de înregistrare."""

    username: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    show_password: bool = False
    agree_terms: bool = False

    def toggle_show_password(self):
        """Comută vizibilitatea parolei."""
        self.show_password = not self.show_password

    def handle_register(self):
        """Gestionează procesul de înregistrare."""
        if (
            not self.username
            or not self.email
            or not self.password
            or not self.confirm_password
        ):
            self.error = "Vă rugăm să completați toate câmpurile."
            return

        if not self.agree_terms:
            self.error = "Trebuie să fiți de acord cu termenii și condițiile."
            return

        if self.password != self.confirm_password:
            self.error = "Parolele nu se potrivesc."
            return

        return self.register(
            self.username, self.email, self.password, self.confirm_password
        )


def register() -> rx.Component:
    """Componenta paginii de înregistrare."""
    return rx.box(
        navbar(),
        rx.center(
            rx.card(
                rx.card_header(
                    rx.heading("Înregistrare", size="lg"),
                ),
                rx.card_body(
                    rx.vstack(
                        rx.cond(
                            State.error,
                            rx.alert(
                                rx.alert_icon(),
                                rx.alert_title(State.error),
                                status="error",
                                mb="4",
                            ),
                        ),
                        rx.form_control(
                            rx.form_label("Nume de utilizator"),
                            rx.input(
                                placeholder="Alegeți un nume de utilizator",
                                on_change=RegisterState.set_username,
                                value=RegisterState.username,
                            ),
                            is_required=True,
                        ),
                        rx.form_control(
                            rx.form_label("Email"),
                            rx.input(
                                placeholder="Introduceți adresa de email",
                                type="email",
                                on_change=RegisterState.set_email,
                                value=RegisterState.email,
                            ),
                            is_required=True,
                        ),
                        rx.form_control(
                            rx.form_label("Parolă"),
                            rx.input_group(
                                rx.input(
                                    placeholder="Alegeți o parolă",
                                    type=rx.cond(
                                        RegisterState.show_password,
                                        "text",
                                        "password",
                                    ),
                                    on_change=RegisterState.set_password,
                                    value=RegisterState.password,
                                ),
                                rx.input_right_element(
                                    rx.icon_button(
                                        rx.cond(
                                            RegisterState.show_password,
                                            "view_off",
                                            "view",
                                        ),
                                        on_click=RegisterState.toggle_show_password,
                                    ),
                                ),
                            ),
                            is_required=True,
                        ),
                        rx.form_control(
                            rx.form_label("Confirmă parola"),
                            rx.input(
                                placeholder="Confirmați parola",
                                type=rx.cond(
                                    RegisterState.show_password,
                                    "text",
                                    "password",
                                ),
                                on_change=RegisterState.set_confirm_password,
                                value=RegisterState.confirm_password,
                            ),
                            is_required=True,
                        ),
                        rx.checkbox(
                            "Sunt de acord cu termenii și condițiile",
                            on_change=RegisterState.set_agree_terms,
                            is_checked=RegisterState.agree_terms,
                        ),
                        rx.button(
                            "Înregistrare",
                            color_scheme="blue",
                            width="100%",
                            on_click=RegisterState.handle_register,
                        ),
                        rx.divider(),
                        rx.text(
                            "Ai deja cont? ",
                            rx.link("Autentifică-te", href="/login", color="blue.500"),
                        ),
                        spacing="4",
                        align_items="start",
                        width="100%",
                    ),
                ),
                width="400px",
            ),
            py="20",
        ),
        footer(),
    )
