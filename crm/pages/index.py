import reflex as rx

from crm.components import crm
from crm.components import navbar
from crm.state import State


def index():
    return rx.vstack(
        navbar(),
        rx.cond(
            State.user,
            crm(),
            rx.vstack(
                rx.heading("Welcome to Vikings!"),
                rx.link(
                    rx.button(
                        "Log in to get started", color_scheme="blue", underline="none"
                    ),
                    href="/login",
                ),
                max_width="500px",
                text_align="center",
                spacing="1rem",
            ),
        ),
        spacing="1.5rem",
    )
