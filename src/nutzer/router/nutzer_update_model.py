"""Pydantic-Model zum Aktualisieren von Nutzerdaten."""

from datetime import date
from typing import Annotated, Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

from nutzer.entity import Rolle, Status, Nutzer

__all__ = ["NutzerUpdateModel"]

class NutzerUpdateModel(BaseModel):
    """Pydantic-Model zum Aktualisieren von Nutzerdaten."""

    vorname: Annotated[
        str,
        StringConstraints(min_length=1, max_length=50),
    ]
    """Der Vorname."""

    nachname: Annotated[
        str,
        StringConstraints(min_length=1, max_length=50),
    ]
    """Der Nachname."""

    email: EmailStr
    """Die eindeutige Emailadresse."""

    telefonnummer: str | None = None
    """Die optionale Telefonnummer."""

    geburtsdatum: date
    """Das Geburtsdatum."""

    beitrittsdatum: date
    """Das Beitrittsdatum."""

    aktiv: bool
    """Aktiv-Status."""

    rolle: Rolle
    """Die Rolle."""

    status: Status
    """Der Status."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "vorname": "Max",
                "nachname": "Mustermann",
                "email": "max@example.com",
                "telefonnummer": "123456789",
                "geburtsdatum": "2000-01-01",
                "beitrittsdatum": "2024-01-01",
                "aktiv": True,
                "rolle": "NUTZER",
                "status": "AKTIV",
            },
        },
    )

    def to_dict(self) -> dict[str, Any]:
        """Konvertierung der primitiven Attribute in ein Dictionary.

        :return: Dictionary mit den primitiven Nutzer-Attributen
        :rtype: dict[str, Any]
        """
        nutzer_dict = self.model_dump()

        # Felder setzen, die nicht aus dem Update kommen
        nutzer_dict["id"] = None
        nutzer_dict["adresse"] = None
        nutzer_dict["einstellung"] = None
        nutzer_dict["interessen"] = []
        nutzer_dict["username"] = None
        nutzer_dict["erzeugt"] = None
        nutzer_dict["aktualisiert"] = None

        return nutzer_dict

    def to_nutzer(self) -> Nutzer:
        """Konvertierung in ein Nutzer-Objekt fuer SQLAlchemy.

        :return: Nutzer-Objekt fuer SQLAlchemy
        :rtype: Nutzer
        """
        logger.debug("self={}", self)

        nutzer_dict = self.to_dict()
        nutzer = Nutzer(**nutzer_dict)

        logger.debug("nutzer={}", nutzer)
        return nutzer
