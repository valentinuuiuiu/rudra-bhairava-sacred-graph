import reflex as rx
import httpx
from frontend_reflex.state import AuthState
from frontend_reflex.components.navbar import navbar

class RegisterFormState(rx.State):
    """Register form state."""
    username: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    loading: bool = False
    error: str = ""
    success: bool = False
    
    def validate(self) -> bool:
        """Validate form inputs."""
        if not self.username:
            self.error = "Username is required"
            return False
        
        if not self.email:
            self.error = "Email is required"
            return False
        
        if not self.password:
            self.error = "Password is required"
            return False
        
        if self.password != self.confirm_password:
            self.error = "Passwords do not match"
            return False
        
        return True
    
    async def handle_submit(self):
        """Handle form submission."""
        if not self.validate():
            return
        
        self.loading = True
        self.error = ""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/api/users/",
                    json={
                        "username": self.username,
                        "email": self.email,
                        "password": self.password,
                    }
                )
                
                if response.status_code == 201:
                    self.success = True
                    # Clear form
                    self.username = ""
                    self.email = ""
                    self.password = ""
                    self.confirm_password = ""
                else:
                    data = response.json()
                    if isinstance(data, dict):
                        # Extract first error message
                        for field, errors in data.items():
                            if isinstance(errors, list) and errors:
                                self.error = f"{field}: {errors[0]}"
                                break
                            elif isinstance(errors, str):
                                self.error = f"{field}: {errors}"
                                break
                    else:
                        self.error = "Registration failed"
        except Exception as e:
            self.error = f"Error: {str(e)}"
        finally:
            self.loading = False


def register() -> rx.Component:
    """The register page."""
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Register", size="2xl", margin_top="2em"),
                rx.text(
                    "Create a new account",
                    color="gray.600",
                    font_size="xl",
                ),
                rx.cond(
                    RegisterFormState.error,
                    rx.alert(
                        rx.alert_icon(),
                        rx.alert_title(RegisterFormState.error),
                        status="error",
                        variant="solid",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    RegisterFormState.success,
                    rx.alert(
                        rx.alert_icon(),
                        rx.alert_title("Registration successful! You can now login."),
                        status="success",
                        variant="solid",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Username",
                            value=RegisterFormState.username,
                            on_change=RegisterFormState.set_username,
                            size="lg",
                            width="100%",
                        ),
                        rx.input(
                            placeholder="Email",
                            type="email",
                            value=RegisterFormState.email,
                            on_change=RegisterFormState.set_email,
                            size="lg",
                            width="100%",
                        ),
                        rx.password(
                            placeholder="Password",
                            value=RegisterFormState.password,
                            on_change=RegisterFormState.set_password,
                            size="lg",
                            width="100%",
                        ),
                        rx.password(
                            placeholder="Confirm Password",
                            value=RegisterFormState.confirm_password,
                            on_change=RegisterFormState.set_confirm_password,
                            size="lg",
                            width="100%",
                        ),
                        rx.button(
                            "Register",
                            type="submit",
                            color_scheme="blue",
                            size="lg",
                            width="100%",
                            is_loading=RegisterFormState.loading,
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=RegisterFormState.handle_submit,
                    width="100%",
                    max_width="400px",
                ),
                rx.text(
                    "Already have an account? ",
                    rx.link("Login", href="/login", color="blue.500"),
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
