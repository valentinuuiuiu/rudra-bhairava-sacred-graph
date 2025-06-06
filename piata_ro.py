"""Piata.ro - O aplicație de marketplace construită cu Reflex și Django."""

import reflex as rx
from rxconfig import config

# Definim starea aplicației
class State(rx.State):
    """Starea de bază pentru aplicația Piata.ro."""
    
    # Starea utilizatorului
    is_authenticated: bool = False
    username: str = ""
    credits: int = 0
    
    # Metode pentru autentificare
    def login(self):
        """Simulare autentificare."""
        self.is_authenticated = True
        self.username = "demo_user"
        self.credits = 10
    
    def logout(self):
        """Deconectare utilizator."""
        self.is_authenticated = False
        self.username = ""
        self.credits = 0

# Componente
def navbar():
    """Bara de navigare pentru Piata.ro."""
    return rx.box(
        rx.hstack(
            rx.heading("Piata.ro", size="md"),
            rx.spacer(),
            rx.cond(
                State.is_authenticated,
                rx.hstack(
                    rx.text(f"Credite: {State.credits}"),
                    rx.button("Deconectare", on_click=State.logout, variant="ghost"),
                    spacing="4",
                ),
                rx.button("Autentificare", on_click=State.login),
            ),
            width="100%",
            padding="4",
        ),
        bg="white",
        border_bottom="1px solid",
        border_color="gray.200",
    )

def footer():
    """Subsolul pentru Piata.ro."""
    return rx.box(
        rx.vstack(
            rx.text("© 2024 Piata.ro. Toate drepturile rezervate."),
            padding="4",
        ),
        bg="gray.100",
        width="100%",
    )

# Pagini
def index():
    """Pagina principală."""
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading("Bine ați venit la Piata.ro", size="2xl"),
                rx.text("Marketplace-ul românesc pentru anunțuri"),
                rx.hstack(
                    rx.input(placeholder="Ce cauți?"),
                    rx.button("Caută", color_scheme="blue"),
                ),
                rx.cond(
                    ~State.is_authenticated,
                    rx.box(
                        rx.alert(
                            rx.alert_icon(),
                            rx.alert_title("Autentifică-te pentru a posta anunțuri"),
                            status="info",
                        ),
                        width="100%",
                        margin_top="4",
                    ),
                ),
                spacing="4",
                padding="10",
                width="100%",
                max_width="800px",
            ),
        ),
        footer(),
    )

def credits():
    """Pagina de credite."""
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading("Credite", size="xl"),
                rx.text(f"Ai {State.credits} credite disponibile."),
                rx.button("Cumpără credite", color_scheme="green"),
                spacing="4",
                padding="10",
                width="100%",
                max_width="800px",
            ),
        ),
        footer(),
    )

# Creează aplicația
app = rx.App()

# Adaugă paginile la aplicație
app.add_page(index, route="/")
app.add_page(credits, route="/credits")
