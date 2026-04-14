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

@strawberry.type
class Query:
    """Queries, um Nutzerdaten zu lesen."""

    @strawberry.field
    def nutzer(self, nutzer_id: strawberry.ID, info: Info) -> NutzerDTO | None:
        """Daten zu einem Nutzer lesen."""
        logger.debug("nutzer_id={}", nutzer_id)

        request: Final[Request] = info.context.get("request")
        user: Final = _token_service.get_user_from_request(request=request)
        if user is None:
            return None

        try:
            nutzer_dto: Final = _service.find_by_id(nutzer_id=int(nutzer_id))
        except NotFoundError:
            return None

        logger.debug("{}", nutzer_dto)
        return nutzer_dto
