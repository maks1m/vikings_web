import reflex as rx


class CrmConfig(rx.Config):
    pass


config = CrmConfig(
    app_name="crm",
    # db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
    db_config=rx.DBConfig(
        engine="postgresql+psycopg2",
        username="admin",
        password="admin",
        host="localhost",
        port=5432,
        database="vikings",
    )
)
