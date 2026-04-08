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

    def __init__(self, repo: NutzerRepository) -> None:
        """Konstruktor mit abhaengigem NutzerRepository."""
        self.repo: NutzerRepository = repo

    def create(self, nutzer: Nutzer) -> NutzerDTO:
        """Einen neuen Nutzer anlegen.

        :param nutzer: Der neue Nutzer ohne ID
        :return: Der neu angelegte Nutzer mit generierter ID
        :rtype: NutzerDTO
        :raises EmailExistsError: Falls die Emailadresse bereits existiert
        :raises UsernameExistsError: Falls der Benutzername bereits existiert
        """
        logger.debug(
            "nutzer={}, adresse={}, einstellung={}",
            nutzer,
            nutzer.adresse,
            nutzer.einstellung,
        )

        with Session() as session:
            email: Final = nutzer.email
            if self.repo.exists_email(email=email, session=session):
                raise EmailExistsError(email=email)

            username: Final = nutzer.username
            if self.repo.exists_username(username=username, session=session):
                raise UsernameExistsError(username)

            nutzer_db: Final = self.repo.create(nutzer=nutzer, session=session)
            nutzer_dto: Final = NutzerDTO(nutzer_db)
            session.commit()

        logger.debug("nutzer_dto={}", nutzer_dto)
        return nutzer_dto
