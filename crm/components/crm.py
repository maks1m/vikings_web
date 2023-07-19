import reflex as rx

from crm.state import State


class CRMState(State):
    vikings: list[dict[str, str]] = []
    name_filter: str = ""

    def on_page_loaded(self):
        print("crm page loaded")
        self.name_filter = ""
        self.get_vikings()

    def get_vikings(self):
        with rx.session() as sess:
            query = """
            select 
                id,
                name, 
                TO_CHAR(updated_at, 'YYYY/MM/DD HH12:MM:SS') 
            from vikings
            """

            if self.name_filter:
                query += f"""
                where name like '%{self.name_filter}%'
                """

            res = sess.execute(query).all()
            self.vikings = [{"id": x[0], "name": x[1], "modified": x[2]} for x in res]

    def set_name_filter(self, value):
        self.name_filter = value
        self.get_vikings()

    @rx.var
    def vikings_count(self):
        return len(self.vikings)


def viking_row(viking: dict):
    print(viking)
    link = "/viking/" + viking["name"]
    return rx.tr(
        rx.td(rx.link(viking["name"], href=link, color="rgb(107,99,246)")),
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
        rx.input(placeholder="Filter by name...", on_change=CRMState.set_name_filter),
        rx.table_container(
            rx.table(rx.tbody(rx.foreach(CRMState.vikings, viking_row))),
            margin_top="1rem",
        ),
        width="100%",
        max_width="960px",
        padding_x="0.5rem",
    )
