import reflex as rx

from crm.components import navbar
from crm.state import State


class VikingState(State):
    _viking_id: str
    movies: list[dict[str, list[str]]]

    @rx.var
    def viking_name(self):
        return self.get_query_params().get("name", None)

    def on_page_loaded(self):
        print("viking page loaded")
        self.get_data()

    def get_data(self):
        with rx.session() as sess:
            self._viking_id = self.get_viking_id(sess)
            print(self._viking_id)

            self.get_movies(sess)
            print(self.movies)

    def get_viking_id(self, sess):
        query = """
            select id 
            from vikings
            where name = :name
            """
        return sess.execute(query, {"name": self.viking_name}).scalar()

    def get_movies(self, sess):
        query = """
            select 
                id,
                name,
                actor_name,
                description 
            from viking_movies
            where viking_id = :id
            """
        print(f"viking ID: {self._viking_id}")
        res = sess.execute(query, {"id": self._viking_id}).all()

        self.movies = [
            {
                "id": x[0],
                "name": x[1],
                "actor_name": x[2],
                "description": x[3],
                "images": []
            } for x in res
        ]

        for m in self.movies:
            query = """
                select image_url
                from viking_images
                where movie_id = :id
                """
            m["images"] = sess.execute(query, {"id": m["id"]}).all()


def image_card(image_url: str):
    return rx.image(
        src=image_url,
        width="auto",
        height="200px",
        border_radius="10px",
        border="2px solid #555",
        box_shadow="lg",

        shadow="lg",
        padding="1em",
    )


def movie_card(movie: dict[str, list[str]]):
    # def images(l) -> list[str]:
    #     return l

    return rx.vstack(
        rx.text(movie["name"], font_size="1.5em", as_="b"),
        rx.text(movie["actor_name"], font_size="1.3em", as_="i"),
        rx.text(movie["description"], font_size="1em", ),
        rx.responsive_grid(
            # rx.foreach(images(movie["images"]), image_card)
            rx.foreach(movie["images"], image_card),
            columns=[1,2,3]
        )
    )


# @rx.route(route="/viking/[name]")
def viking():
    return rx.vstack(
        navbar(),
        rx.heading(VikingState.viking_name),
        rx.foreach(VikingState.movies, movie_card),
        text_align="top",
        position="relative",
    )
