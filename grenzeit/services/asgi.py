from fastapi import FastAPI
from neomodel import config
from uvicorn import Server, Config
from uvicorn.supervisors import ChangeReload

from grenzeit.api_v1.main import api_v1
from grenzeit.config import settings
from grenzeit.logging import setup_logging

config.DATABASE_URL = settings.DATABASE_URL

app = FastAPI()

app.mount('/api/v1', api_v1)


class FixedLoggingConfig(Config):
    """Subclass of uvicorn config that re-configures logging."""

    serialize_logs = False

    def configure_logging(self) -> None:  # noqa: D102
        super().configure_logging()
        setup_logging()


if __name__ == "__main__":
    config = FixedLoggingConfig(
        "grenzeit.services.asgi:app",
        host=settings.HOSTNAME,
        log_level=settings.LOG_LEVEL,
        port=settings.HOST_PORT,
        reload=settings.DEBUG
    )
    server = Server(
        config
    )

    if settings.DEBUG:
        sock = config.bind_socket()
        ChangeReload(config, target=server.run, sockets=[sock]).run()
    else:
        server.run()