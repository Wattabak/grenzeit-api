from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from neomodel import config
from uvicorn import Server, Config
from uvicorn.supervisors import ChangeReload

from grenzeit.api.v1.main import v1
from grenzeit.config import settings
from grenzeit.logging import setup_logging

config.DATABASE_URL = settings.DATABASE_URL


def create_app():
    app = FastAPI()

    app.mount("/api/v1", v1)

    app.mount("/api/latest", v1)

    @app.get("/")
    async def docs_redirect():
        return RedirectResponse(url='/api/latest/redoc')

    return app


class FixedLoggingConfig(Config):
    """Subclass of uvicorn config that re-configures logging."""

    serialize_logs = False

    def configure_logging(self) -> None:  # noqa: D102
        super().configure_logging()
        setup_logging()


app = create_app()

if __name__ == "__main__":
    config = FixedLoggingConfig(
        "grenzeit.services.asgi:app",
        host=settings.HOSTNAME,
        log_level=settings.LOG_LEVEL,
        port=settings.HOST_PORT,
        reload=settings.DEBUG
    )
    server = Server(config)

    if settings.DEBUG:
        sock = config.bind_socket()
        ChangeReload(config, target=server.run, sockets=[sock]).run()
    else:
        server.run()
