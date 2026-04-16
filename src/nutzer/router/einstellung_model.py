"""Pydantic-Model fuer die Einstellungen eines Nutzers."""

from typing import Annotated

from loguru import logger
from pydantic import BaseModel, ConfigDict, StringConstraints

from nutzer.entity import Einstellung

__all__ = ["EinstellungModel"]


class EinstellungModel(BaseModel):
    """Pydantic-Model fuer die Einstellungen eines Nutzers."""

    newsletter_aktiv: bool
    """Ob der Newsletter aktiv ist."""

    benachrichtigungen_aktiv: bool
    """Ob Benachrichtigungen aktiv sind."""

    sprache: Annotated[str, StringConstraints(min_length=1, max_length=20)]
    """Die Sprache."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "newsletter_aktiv": True,
                "benachrichtigungen_aktiv": True,
                "sprache": "de",
            },
        }
    )

    def to_einstellung(self) -> Einstellung:
        """Konvertierung in ein Einstellung-Objekt fuer SQLAlchemy.

        :return: Einstellung-Objekt fuer SQLAlchemy
        :rtype: Einstellung
        """
        logger.debug("self={}", self)
        einstellung_dict = self.model_dump()
        einstellung_dict["id"] = None
        einstellung_dict["nutzer_id"] = None
        einstellung_dict["nutzer"] = None

        einstellung = Einstellung(**einstellung_dict)
        logger.debug("einstellung={}", einstellung)
        return einstellung
