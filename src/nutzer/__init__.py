"""Package fuer das neue Nutzer-Projekt."""

from nutzer.asgi_server import run
from nutzer.fastapi_app import app

__all__ = ["app", "main"]


def main() -> None:
    """Paket als Skript starten."""
    run()
