import reflex as rx

from frontend_reflex.state import AuthState


def navbar() -> rx.Component:
    """The navbar component."""
    return rx.hstack(
        rx.hstack(
            rx.heading("Piata.ro", size="lg", color="blue.500"),
            rx.spacer(),
            rx.hstack(
                rx.link("Home", href="/", color="gray.800"),
                rx.cond(
                    AuthState.user.is_none(),
                    rx.hstack(
                        rx.link("Login", href="/login", color="gray.800"),
                        rx.link("Register", href="/register", color="gray.800"),
                    ),
                    rx.hstack(
                        rx.link("My Account", href="/account", color="gray.800"),
                        rx.link("Post Ad", href="/post", color="gray.800"),
                        rx.link("Favorites", href="/favorites", color="gray.800"),
                        rx.link("Messages", href="/messages", color="gray.800"),
                        rx.button(
                            "Logout",
                            on_click=AuthState.logout,
                            variant="ghost",
                            color="gray.800",
                        ),
                    ),
                ),
                spacing="4",
            ),
            width="100%",
            max_width="1200px",
        ),
        width="100%",
        padding="4",
        border_bottom="1px solid",
        border_color="gray.200",
        position="sticky",
        top="0",
        z_index="999",
        background_color="white",
    )
