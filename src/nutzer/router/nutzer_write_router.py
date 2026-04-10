"""NutzerWriteRouter."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from nutzer.problem_details import create_problem_details
from nutzer.router.constants import ETAG, IF_MATCH, IF_MATCH_MIN_LEN
from nutzer.router.dependencies import get_write_service
from nutzer.router.nutzer_model import NutzerModel
from nutzer.router.nutzer_update_model import NutzerUpdateModel
from nutzer.security import Role, RolesRequired
from nutzer.service.nutzer_write_service import NutzerWriteService
