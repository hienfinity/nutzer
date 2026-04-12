"""Gemeinsame Basisklasse fuer alle Entities der Domaene Nutzer."""

from typing import TYPE_CHECKING, Any

from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:

    class MappedAsDataclass:
        """Hilfstyp fuer Typhinweise ohne Laufzeitimport."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Beschreibt die Signatur des Mixins fuer den Type-Checker."""

else:
    from sqlalchemy.orm import MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """Basisklasse fuer SQLAlchemy-Entities als Dataclasses."""
