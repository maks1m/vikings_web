import reflex as rx


class CrmConfig(rx.Config):
    pass


config = CrmConfig(
    app_name="crm",
    env=rx.Env.DEV,
    api_url="http://0.0.0.0:8000",
    bun_path="/app/.bun/bin/bun",
    db_config=rx.DBConfig(
        engine="postgresql+psycopg2",
        username="admin",
        password="admin",
        # host="localhost",
        host="viking-db",
        port=5432,
        database="vikings",
    ),
    telemetry_enabled=False,
)
