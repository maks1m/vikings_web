import reflex as rx

from crm.components import navbar
from crm.state import State


class VikingState(State):

    @rx.var
    def viking_name(self):
        return self.get_query_params().get("name", None)


@rx.route(route="/viking/[name]")
def viking():
    return rx.vstack(
        navbar(),
        rx.heading(VikingState.viking_name)
    )
