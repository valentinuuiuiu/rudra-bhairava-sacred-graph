"""Starea aplicației pentru Piata.ro."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import httpx
import reflex as rx


class State(rx.State):
    """Starea de bază pentru aplicația Piata.ro."""

    # Starea utilizatorului
    is_authenticated: bool = False
    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None

    # Credite și abonament
    credits: int = 0
    subscription_type: Optional[str] = None
    subscription_expires: Optional[datetime] = None

    # Starea de încărcare
    is_loading: bool = False
    error: Optional[str] = None

    # URL-ul API-ului backend
    api_url: str = "http://localhost:8000/api"

    async def login(self, username: str, password: str):
        """Autentificare utilizator."""
        self.is_loading = True
        self.error = None

        try:
            # În producție, se va conecta la API-ul Django
            # Simulare pentru dezvoltare
            if username == "demo" and password == "demo123":
                self.is_authenticated = True
                self.user_id = 1
                self.username = username
                self.email = "demo@example.com"
                self.credits = 10
                self.subscription_type = "Basic"
                self.subscription_expires = datetime.now() + timedelta(days=30)
                self.is_loading = False
                return rx.redirect("/")
            else:
                self.error = "Nume de utilizator sau parolă incorecte."
        except Exception as e:
            self.error = f"Eroare la autentificare: {str(e)}"

        self.is_loading = False

    def logout(self):
        """Deconectare utilizator."""
        self.is_authenticated = False
        self.user_id = None
        self.username = None
        self.email = None
        self.credits = 0
        self.subscription_type = None
        self.subscription_expires = None
        return rx.redirect("/login")

    async def register(
        self, username: str, email: str, password: str, confirm_password: str
    ):
        """Înregistrare utilizator nou."""
        self.is_loading = True
        self.error = None

        if password != confirm_password:
            self.error = "Parolele nu se potrivesc."
            self.is_loading = False
            return

        try:
            # În producție, se va conecta la API-ul Django
            # Simulare pentru dezvoltare
            self.is_authenticated = True
            self.user_id = 1
            self.username = username
            self.email = email
            self.credits = 5  # Credite gratuite pentru utilizatorii noi
            self.is_loading = False
            return rx.redirect("/")
        except Exception as e:
            self.error = f"Eroare la înregistrare: {str(e)}"
            self.is_loading = False

    async def buy_credits(self, amount: int, payment_method: str):
        """Cumpără credite."""
        self.is_loading = True
        self.error = None

        try:
            # În producție, se va conecta la API-ul Django pentru procesarea plății
            # Simulare pentru dezvoltare
            self.credits += amount
            self.is_loading = False
            return rx.window_alert(f"Ai cumpărat cu succes {amount} credite!")
        except Exception as e:
            self.error = f"Eroare la cumpărarea creditelor: {str(e)}"
            self.is_loading = False

    async def upgrade_subscription(self, plan: str):
        """Actualizează abonamentul utilizatorului."""
        self.is_loading = True
        self.error = None

        plans = {
            "basic": {"name": "Basic", "duration": 30, "credits": 10},
            "premium": {"name": "Premium", "duration": 30, "credits": 50},
            "business": {"name": "Business", "duration": 30, "credits": 200},
        }

        if plan not in plans:
            self.error = "Plan de abonament invalid."
            self.is_loading = False
            return

        try:
            # În producție, se va conecta la API-ul Django pentru procesarea plății
            # Simulare pentru dezvoltare
            self.subscription_type = plans[plan]["name"]
            self.subscription_expires = datetime.now() + timedelta(
                days=plans[plan]["duration"]
            )
            self.credits += plans[plan]["credits"]
            self.is_loading = False
            return rx.window_alert(
                f"Abonament {plans[plan]['name']} activat cu succes!"
            )
        except Exception as e:
            self.error = f"Eroare la actualizarea abonamentului: {str(e)}"
            self.is_loading = False
