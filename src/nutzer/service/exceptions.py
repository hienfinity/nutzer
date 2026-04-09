"""Exceptions in der Geschaeftslogik von Nutzer."""

__all__ = [
    "NotFoundError",
    "EmailExistsError",
    "UsernameExistsError",
    "VersionOutdatedError",
]

class NotFoundError(Exception):
    """Exception, falls kein Nutzer gefunden wurde."""

    def __init__(self, nutzer_id: int | None = None) -> None:
        """Initialisierung mit der nicht gefundenen Nutzer-ID."""
        super().__init__("Not Found")
        self.nutzer_id = nutzer_id

class EmailExistsError(Exception):
    """Exception, falls die Emailadresse bereits existiert."""

    def __init__(self, email: str) -> None:
        """Initialisierung mit der existierenden Emailadresse."""
        super().__init__("Email already exists")
        self.email = email

class UsernameExistsError(Exception):
    """Exception, falls der Benutzername bereits existiert."""

    def __init__(self, username: str) -> None:
        """Initialisierung mit dem existierenden Benutzernamen."""
        super().__init__("Username already exists")
        self.username = username
