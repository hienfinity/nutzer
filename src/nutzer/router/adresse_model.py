"""Pydantic-Model fuer die Adresse eines Nutzers."""

from typing import Annotated

from loguru import logger
from pydantic import BaseModel, ConfigDict, StringConstraints

from nutzer.entity import Adresse

__all__ = ["AdresseModel"]


class AdresseModel(BaseModel):
    """Pydantic-Model fuer die Adresse eines Nutzers."""

    strasse: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    """Die Strasse."""

    hausnummer: Annotated[str, StringConstraints(min_length=1, max_length=10)]
    """Die Hausnummer."""

    plz: Annotated[str, StringConstraints(min_length=1, max_length=10)]
    """Die Postleitzahl."""

    ort: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    """Der Ort."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "strasse": "Hauptstrasse",
                "hausnummer": "12a",
                "plz": "76133",
                "ort": "Karlsruhe",
            },
        }
    )

    def to_adresse(self) -> Adresse:
        """Konvertierung in ein Adresse-Objekt fuer SQLAlchemy.

        :return: Adresse-Objekt fuer SQLAlchemy
        :rtype: Adresse
        """
        logger.debug("self={}", self)
        adresse_dict = self.model_dump()
        adresse_dict["id"] = None
        adresse_dict["nutzer"] = None

        adresse = Adresse(**adresse_dict)
        logger.debug("adresse={}", adresse)
        return adresse
