"""Factory-Funktionen fuer Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from nutzer.repository.nutzer_repository import NutzerRepository
from nutzer.security.dependencies import get_user_service
from nutzer.security.user_service import UserService
from nutzer.service.nutzer_service import NutzerService
from nutzer.service.nutzer_write_service import NutzerWriteService

__all__ = ["get_repository", "get_service", "get_write_service"]

def get_repository() -> NutzerRepository:
    """Factory-Funktion fuer NutzerRepository.

    :return: Das Repository
    :rtype: NutzerRepository
    """
    return NutzerRepository()

def get_service(
    repo: Annotated[NutzerRepository, Depends(get_repository)],
) -> NutzerService:
    """Factory-Funktion fuer NutzerService."""
    return NutzerService(repo=repo)

