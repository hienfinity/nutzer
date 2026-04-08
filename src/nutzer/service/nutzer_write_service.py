"""Geschaeftslogik zum Schreiben von Nutzerdaten."""

from typing import Final

from loguru import logger

from nutzer.entity import Nutzer
from nutzer.repository import NutzerRepository, Session
from nutzer.service.exceptions import (
    EmailExistsError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)
from nutzer.service.nutzer_dto import NutzerDTO

__all__ = ["NutzerWriteService"]
class NutzerWriteService:
    """Service-Klasse mit Geschaeftslogik fuer Nutzer."""