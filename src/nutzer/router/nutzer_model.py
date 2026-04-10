"""Pydantic-Model fuer die Nutzerdaten."""

from typing import Annotated, Final

from loguru import logger
from pydantic import StringConstraints

from nutzer.entity import Interesse, Nutzer
from nutzer.router.adresse_model import AdresseModel
from nutzer.router.einstellung_model import EinstellungModel
from nutzer.router.nutzer_update_model import NutzerUpdateModel

__all__ = ["NutzerModel"]
