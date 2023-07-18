from datetime import datetime

import reflex as rx

from crm.state import State


class CRMState(State):
    vikings: list[dict] = []
    name_filter: str = ""

    def get_vikings(self):
        with rx.session() as sess:
            query = """
            select 
                name, 
                TO_CHAR(updated_at, 'YYYY/MM/DD HH12:MM:SS') 
            from vikings
            """

            if self.name_filter:
                query += f"""
                where name like '%{self.name_filter}%'
                """

            res = sess.execute(query).all()
            self.vikings = [{"name": x[0], "modified": x[1]} for x in res]

    def set_name_filter(self, value):
        self.name_filter = value
        self.get_vikings()

    @rx.var
    def vikings_count(self):
        return len(self.vikings)

    # @rx.var
    # def vikings(self) -> list[tuple[str, datetime]]:
    #     return self.contacts()


# class AddModalState(CRMState):
#     show: bool = False
#     name: str = ""
#     email: str = ""
#
#     def toggle(self):
#         self.show = not self.show
#
#     def add_contact(self):
#         if not self.user:
#             raise ValueError("No user logged in")
#         with rx.session() as sess:
#             sess.expire_on_commit = False
#             sess.add(
#                 Contact(
#                     user_email=self.user.email, contact_name=self.name, email=self.email
#                 )
#             )
#             sess.commit()
#             self.toggle()
#             return self.get_contacts()


# def add_modal():
#     return rx.modal(
#         rx.modal_overlay(
#             rx.modal_content(
#                 rx.modal_header("Add"),
#                 rx.modal_body(
#                     rx.input(
#                         on_change=AddModalState.set_name,
#                         placeholder="Name",
#                         margin_bottom="0.5rem",
#                     ),
#                     rx.input(on_change=AddModalState.set_email, placeholder="Email"),
#                     padding_y=0,
#                 ),
#                 rx.modal_footer(
#                     rx.button("Close", on_click=AddModalState.toggle),
#                     rx.button(
#                         "Add", on_click=AddModalState.add_contact, margin_left="0.5rem"
#                     ),
#                 ),
#             )
#         ),
#         is_open=AddModalState.show,
#     )


def viking_row(viking: dict):
    print(viking)
    return rx.tr(
        rx.td(viking["name"]),
        rx.td(viking["modified"]),
        # rx.td(rx.badge(viking.stage)),
    )


def crm():
    return rx.box(
        rx.button("Refresh", on_click=CRMState.get_vikings),
        rx.hstack(
            rx.heading("Vikings"),
            # rx.button("Add", on_click=AddModalState.toggle),
            justify_content="space-between",
            align_items="flex-start",
            margin_bottom="1rem",
        ),
        rx.responsive_grid(
            rx.box(
                rx.stat(
                    rx.stat_label("Total count"), rx.stat_number(CRMState.vikings_count)
                ),
                border="1px solid #eaeaef",
                padding="1rem",
                border_radius=8,
            ),
            columns=["5"],
            margin_bottom="1rem",
        ),
        # add_modal(),
        rx.input(placeholder="Filter by name...", on_change=CRMState.set_name_filter),
        rx.table_container(
            rx.table(rx.tbody(rx.foreach(CRMState.vikings, viking_row))),
            margin_top="1rem",
        ),
        width="100%",
        max_width="960px",
        padding_x="0.5rem",
    )
