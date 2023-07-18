"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx

from crm.components.crm import CRMState
from crm.pages import index, login, viking
from crm.state import State


# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index, on_load=CRMState.get_vikings())
app.add_page(login)
# app.add_page(viking, route="/viking/[name]")
app.compile()
