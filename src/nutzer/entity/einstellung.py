"""Entity-Klasse fuer Einstellungen eines Nutzers."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nutzer.entity.base import Base

if TYPE_CHECKING:
    from nutzer.entity.nutzer import Nutzer


class Einstellung(Base):
    """Persoenliche Einstellungen eines Nutzers."""

    __tablename__ = "einstellung"

    newsletter_aktiv: Mapped[bool]
    """Gibt an, ob der Newsletter aktiviert ist."""

    benachrichtigungen_aktiv: Mapped[bool]
    """Gibt an, ob Benachrichtigungen aktiviert sind."""

    sprache: Mapped[str]
    """Die bevorzugte Sprache des Nutzers."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID der Einstellung."""

    nutzer_id: Mapped[int] = mapped_column(ForeignKey("nutzer.id"), unique=True)
    """Die ID des zugehoerigen Nutzers als Fremdschluessel."""

    nutzer: Mapped["Nutzer"] = relationship(back_populates="einstellung")
    """Das zugehoerige Nutzer-Objekt."""

    def __repr__(self) -> str:
        """Einfache Textdarstellung ohne weitere Beziehungen."""
        return (
            "Einstellung("
            f"id={self.id}, nutzer_id={self.nutzer_id}, "
            f"newsletter_aktiv={self.newsletter_aktiv}, "
            f"benachrichtigungen_aktiv={self.benachrichtigungen_aktiv}, "
            f"sprache={self.sprache})"
        )
