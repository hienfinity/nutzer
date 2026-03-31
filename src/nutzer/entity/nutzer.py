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

    beitrittsdatum: Mapped[date]
    """Das Beitrittsdatum."""

    rolle: Mapped[Rolle]
    """Die Rolle."""

    status: Mapped[Status]
    """Der Status."""

    interessen: InitVar[list[Interesse] | None]
    """Die transiente Liste mit Interessen als Enum-Werte."""

    username: Mapped[str] = mapped_column(unique=True)
    """Der eindeutige Benutzername."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    email: Mapped[str] = mapped_column(unique=True)
    """Die eindeutige Emailadresse."""

    adresse: Mapped[Adresse] = relationship(
        back_populates="nutzer",
        innerjoin=True,
        cascade="save-update, delete",
    )
    """Die in einer 1:1-Beziehung referenzierte Adresse."""

    konten: Mapped[list[Konto]] = relationship(
        back_populates="nutzer",
        cascade="save-update, delete",
    )
    """Die in einer 1:N-Beziehung referenzierten Konten."""

    interessen_json: Mapped[list[str] | None] = mapped_column(
        JSON,
        name="interessen",
        init=False,
    )
    """Die persistente Liste der Interessen für ein JSON-Array."""

    version: Mapped[int] = mapped_column(nullable=False, default=0)
    """Die Versionsnummer für optimistische Synchronisation."""

    erzeugt: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        default=None,
    )
    """Der Zeitstempel für das initiale INSERT in die DB-Tabelle."""

    aktualisiert: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default=None,
    )
    """Der Zeitstempel vom letzten UPDATE in der DB-Tabelle."""

    __mapper_args__ = {"version_id_col": version}

    def __post_init__(
        self,
        interessen: list[Interesse] | None,
    ) -> None:
        """Für SQLAlchemy: JSON-Array für DB-Spalte setzen für INSERT oder UPDATE.

        :param interessen: Liste mit Interessen als Enum
        """
        logger.debug("interessen={}", interessen)
        logger.debug("self={}", self)
        self.interessen_json = (
            [interesse_enum.name for interesse_enum in interessen]
            if interessen is not None
            else None
        )
        logger.debug("self.interessen_json={}", self.interessen_json)

    @reconstructor
    def on_load(self) -> None:
        """Auslesen aus der DB: die Enum-Liste durch die DB-Strings initialisieren."""
        self.interessen = (  # pyright: ignore[reportAttributeAccessIssue]
            [Interesse[interesse_name] for interesse_name in self.interessen_json]
            if self.interessen_json is not None
            else []
        )
        logger.debug(
            "interessen={}",
            self.interessen,  # pyright: ignore[reportAttributeAccessIssue]
        )

