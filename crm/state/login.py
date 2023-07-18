import reflex as rx

from .models import User
from .state import State


class LoginState(State):
    """State for the login form."""

    email_field: str = ""
    password_field: str = ""

    def log_in(self):
        with rx.session() as sess:
            user = sess.exec(User.select.where(User.email == self.email_field)).first()
            if user and user.password == self.password_field:
                self.user = user
                return rx.redirect("/")
            else:
                return rx.window_alert("Wrong username or password.")

    def log_out(self):
        self.user = None
        return rx.redirect("/")
