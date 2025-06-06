import reflex as rx
from frontend_reflex.state import AuthState
from frontend_reflex.components.navbar import navbar

class LoginFormState(rx.State):
    """Login form state."""
    username: str = ""
    password: str = ""
    
    def handle_submit(self):
        """Handle form submission."""
        return AuthState.login(self.username, self.password)


def login() -> rx.Component:
    """The login page."""
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Login", size="2xl", margin_top="2em"),
                rx.text(
                    "Sign in to your account",
                    color="gray.600",
                    font_size="xl",
                ),
                rx.cond(
                    AuthState.error,
                    rx.alert(
                        rx.alert_icon(),
                        rx.alert_title(AuthState.error),
                        status="error",
                        variant="solid",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Username",
                            value=LoginFormState.username,
                            on_change=LoginFormState.set_username,
                            size="lg",
                            width="100%",
                        ),
                        rx.password(
                            placeholder="Password",
                            value=LoginFormState.password,
                            on_change=LoginFormState.set_password,
                            size="lg",
                            width="100%",
                        ),
                        rx.button(
                            "Login",
                            type="submit",
                            color_scheme="blue",
                            size="lg",
                            width="100%",
                            is_loading=AuthState.loading,
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=LoginFormState.handle_submit,
                    width="100%",
                    max_width="400px",
                ),
                rx.text(
                    "Don't have an account? ",
                    rx.link("Register", href="/register", color="blue.500"),
                    margin_top="2em",
                ),
                spacing="6",
                padding_y="4",
                width="100%",
                max_width="400px",
                align_items="center",
            ),
            padding_x="4",
        ),
        width="100%",
        min_height="100vh",
        spacing="0",
    )
