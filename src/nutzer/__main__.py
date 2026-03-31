"""CLI-Einstiegspunkt fuer `python -m nutzer`."""

from nutzer.asgi_server import run

__all__ = ["run"]

if __name__ == "__main__":
    run()
