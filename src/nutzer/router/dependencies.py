"""Factory-Funktionen fuer Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from nutzer.repository.nutzer_repository import NutzerRepository
from nutzer.service.nutzer_service import NutzerService
from nutzer.service.nutzer_write_service import NutzerWriteService

__all__ = ["get_repository", "get_service", "get_write_service"]
