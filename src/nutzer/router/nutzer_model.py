"""Pydantic-Model fuer die Nutzerdaten."""

from typing import Annotated, Final

from loguru import logger
from pydantic import StringConstraints

from nutzer.entity import Interesse, Nutzer
from nutzer.router.adresse_model import AdresseModel
from nutzer.router.einstellung_model import EinstellungModel
from nutzer.router.nutzer_update_model import NutzerUpdateModel

__all__ = ["NutzerModel"]

class NutzerModel(NutzerUpdateModel):
    """Pydantic-Model fuer die Nutzerdaten."""

    adresse: AdresseModel
    """Die zugehoerige Adresse."""

    einstellung: EinstellungModel
    """Die zugehoerige Einstellung."""

    interessen: list[Interesse]
    """Die Liste mit Interessen als Enum-Werte."""

    username: Annotated[str, StringConstraints(max_length=20)]
    """Der Benutzername fuer Login."""

    def to_nutzer(self) -> Nutzer:
        """Konvertierung in ein Nutzer-Objekt fuer SQLAlchemy.

        :return: Nutzer-Objekt fuer SQLAlchemy
        :rtype: Nutzer
        """
        logger.debug("self={}", self)
        nutzer_dict = self.to_dict()
        nutzer_dict["interessen"] = self.interessen
        # bei Updates wird "username" nicht aktualisiert bzw. muss gleich bleiben
        # in NutzerUpdateModel wird "username" deshalb nicht gesetzt
        nutzer_dict["username"] = self.username

        nutzer: Final = Nutzer(**nutzer_dict)
        nutzer.adresse = self.adresse.to_adresse()
        nutzer.einstellung = self.einstellung.to_einstellung()
        logger.debug("nutzer={}", nutzer)
        return nutzer
