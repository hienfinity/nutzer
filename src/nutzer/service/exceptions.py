"""Exceptions in der Geschaeftslogik von Nutzer."""

__all__ = ["NotFoundError"]


class NotFoundError(Exception):
    """Exception, falls kein Nutzer gefunden wurde."""

    def __init__(self, nutzer_id: int | None = None) -> None:
        """Initialisierung mit der nicht gefundenen Nutzer-ID."""
        super().__init__("Not Found")
        self.nutzer_id = nutzer_id
