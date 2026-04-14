"""Schema fuer GraphQL durch Strawberry."""

from collections.abc import Sequence
from typing import Final

import strawberry
from fastapi import Request
from loguru import logger
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from nutzer.config.graphql import graphql_ide
from nutzer.graphql_api.graphql_types import (
    CreatePayload,
    LoginResult,
    NutzerInput,
    Suchparameter,
)
from nutzer.repository import Pageable, NutzerRepository
from nutzer.router.nutzer_model import NutzerModel
from nutzer.security import Role, TokenService, UserService
from nutzer.service import (
    NotFoundError,
    NutzerDTO,
    NutzerService,
    NutzerWriteService,
)

__all__ = ["graphql_router"]


_repo: Final = NutzerRepository()
_service: Final = NutzerService(repo=_repo)
_user_service: Final = UserService()
_write_service: Final = NutzerWriteService(
    repo=_repo,
    user_service=_user_service,
)
_token_service: Final = TokenService()