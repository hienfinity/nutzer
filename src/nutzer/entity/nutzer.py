"""Entity-Klasse für Nutzerdaten."""

from dataclasses import InitVar
from datetime import date, datetime
from typing import Any, Self

from loguru import logger
from sqlalchemy import JSON, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, reconstructor, relationship

from nutzer.entity.adresse import Adresse
from nutzer.entity.base import Base
from nutzer.entity.interesse import Interesse
from nutzer.entity.konto import Konto
from nutzer.entity.rolle import Rolle
from nutzer.entity.status import Status

class Nutzer(Base):
    """Entity-Klasse für Nutzerdaten."""

    __tablename__ = "nutzer"

    vorname: Mapped[str]
    """Der Vorname."""

    nachname: Mapped[str]
    """Der Nachname."""

    telefonnummer: Mapped[str | None]
    """Die optionale Telefonnummer."""

    geburtsdatum: Mapped[date]
    """Das Geburtsdatum."""
