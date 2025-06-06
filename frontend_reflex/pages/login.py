"""Pagina de autentificare pentru aplicația de marketplace Piata.ro."""

import reflex as rx

from frontend_reflex.components.navbar import navbar
from frontend_reflex.components.footer import footer
from frontend_reflex.state import State


class LoginState(State):
    """Starea pentru pagina de autentificare."""
    
    username: str = ""
    password: str = ""
    show_password: bool = False
    
    def toggle_show_password(self):
        """Comută vizibilitatea parolei."""
        self.show_password = not self.show_password
    
    def handle_login(self):
        """Gestionează procesul de autentificare."""
        if not self.username or not self.password:
            self.error = "Vă rugăm să completați toate câmpurile."
            return
        
        return self.login(self.username, self.password)


def login() -> rx.Component:
    """Componenta paginii de autentificare."""
    return rx.box(
        navbar(),
        
        rx.center(
            rx.card(
                rx.card_header(
                    rx.heading("Autentificare", size="lg"),
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
                                placeholder="Introduceți numele de utilizator",
                                on_change=LoginState.set_username,
                                value=LoginState.username,
                            ),
                            is_required=True,
                        ),
                        rx.form_control(
                            rx.form_label("Parolă"),
                            rx.input_group(
                                rx.input(
                                    placeholder="Introduceți parola",
                                    type=rx.cond(
                                        LoginState.show_password,
                                        "text",
                                        "password",
                                    ),
                                    on_change=LoginState.set_password,
                                    value=LoginState.password,
                                ),
                                rx.input_right_element(
                                    rx.icon_button(
                                        rx.cond(
                                            LoginState.show_password,
                                            "view_off",
                                            "view",
                                        ),
                                        on_click=LoginState.toggle_show_password,
                                    ),
                                ),
                            ),
                            is_required=True,
                        ),
                        rx.hstack(
                            rx.checkbox("Ține-mă conectat"),
                            rx.spacer(),
                            rx.link("Ai uitat parola?", href="/forgot-password"),
                            width="100%",
                        ),
                        rx.button(
                            "Autentificare",
                            color_scheme="blue",
                            width="100%",
                            on_click=LoginState.handle_login,
                        ),
                        rx.divider(),
                        rx.text(
                            "Nu ai cont? ",
                            rx.link("Înregistrează-te", href="/register", color="blue.500"),
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
