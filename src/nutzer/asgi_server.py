"""Startfunktion fuer die FastAPI-Anwendung mit uvicorn."""

from ssl import PROTOCOL_TLS_SERVER

import uvicorn

from nutzer.config import host_binding, port, tls_certfile, tls_keyfile
from nutzer.fastapi_app import app  # noqa: F401

__all__ = ["run"]


def run() -> None:
    """Anwendung mit uvicorn starten."""
    uvicorn.run(
        "nutzer:app",
        loop="asyncio",
        http="h11",
        interface="asgi3",
        host=host_binding,
        port=port,
        ssl_keyfile=tls_keyfile,
        ssl_certfile=tls_certfile,
        ssl_version=PROTOCOL_TLS_SERVER,
    )
