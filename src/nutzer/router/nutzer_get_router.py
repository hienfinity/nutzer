"""NutzerGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from nutzer.repository import Pageable
from nutzer.repository.slice import Slice
from nutzer.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from nutzer.router.dependencies import get_service
from nutzer.router.page import Page
from nutzer.security import Role, RolesRequired, User
from nutzer.service.nutzer_dto import NutzerDTO
from nutzer.service.nutzer_service import NutzerService

__all__ = ["nutzer_router"]
