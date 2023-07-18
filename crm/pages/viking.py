import reflex as rx

from crm.components import navbar


def viking():
    return rx.vstack(
        navbar(),
        rx.box()
    )
