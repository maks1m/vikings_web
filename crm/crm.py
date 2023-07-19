"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx

from crm.components.crm import CRMState
from crm.pages import index, login, viking
from crm.pages.viking import VikingState
from crm.state import State


# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index, on_load=CRMState.on_page_loaded)
app.add_page(login)
app.add_page(viking, route="/viking/[name]", on_load=VikingState.on_page_loaded)
app.compile()
