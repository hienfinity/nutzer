"""Entity-Klasse fuer eine Adresse in der Domaene Nutzer."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nutzer.entity.base import Base

if TYPE_CHECKING:
    from nutzer.entity.nutzer import Nutzer


class Adresse(Base):
    """Eine postalische Adresse eines Nutzers."""

    __tablename__ = "adresse"

    strasse: Mapped[str]
    """Der Strassenname."""

    hausnummer: Mapped[str]
    """Die Hausnummer."""

    plz: Mapped[str]
    """Die Postleitzahl."""

    ort: Mapped[str]
    """Der Ort."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID der Adresse."""

    nutzer_id: Mapped[int] = mapped_column(ForeignKey("nutzer.id"), unique=True)
    """Die ID des zugehoerigen Nutzers als Fremdschluessel."""

    nutzer: Mapped[Nutzer] = relationship(back_populates="adresse")
    """Das zugehoerige Nutzer-Objekt."""

    def __repr__(self) -> str:
        """Einfache Textdarstellung ohne weitere Beziehungen."""
        return (
            f"Adresse(id={self.id}, nutzer_id={self.nutzer_id}, strasse={self.strasse}, "
            f"hausnummer={self.hausnummer}, plz={self.plz}, ort={self.ort})"
        )
