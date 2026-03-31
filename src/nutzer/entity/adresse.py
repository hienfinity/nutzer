"""Entity-Klasse fuer eine Adresse in der Domaene Nutzer."""

from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column

from nutzer.entity.base import Base


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

    def __repr__(self) -> str:
        """Einfache Textdarstellung ohne weitere Beziehungen."""
        return (
            f"Adresse(id={self.id}, strasse={self.strasse}, "
            f"hausnummer={self.hausnummer}, plz={self.plz}, ort={self.ort})"
        )
