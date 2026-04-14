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

    @strawberry.field
    def nutzer_liste(
        self,
        suchparameter: Suchparameter,
        info: Info,
    ) -> Sequence[NutzerDTO]:
        """Nutzer anhand von Suchparametern suchen."""
        logger.debug("suchparameter={}", suchparameter)

        request: Final[Request] = info.context["request"]
        user: Final = _token_service.get_user_from_request(request)
        if user is None or Role.ADMIN not in user.roles:
            return []

        suchparameter_dict: Final[dict[str, str | None]] = dict(vars(suchparameter))
        suchparameter_filtered = {
            key: value
            for key, value in suchparameter_dict.items()
            if value is not None and value
        }
        logger.debug("suchparameter_filtered={}", suchparameter_filtered)

        pageable: Final = Pageable.create(size=str(0))
        try:
            nutzer_dto: Final = _service.find(
                suchparameter=suchparameter_filtered,
                pageable=pageable,
            )
        except NotFoundError:
            return []

        logger.debug("{}", nutzer_dto)
        return nutzer_dto.content

    @strawberry.mutation
    def create(self, nutzer_input: NutzerInput) -> CreatePayload:
        """Einen neuen Nutzer anlegen."""
        logger.debug("nutzer_input={}", nutzer_input)

        nutzer_dict = nutzer_input.__dict__
        nutzer_dict["adresse"] = nutzer_input.adresse.__dict__
        nutzer_dict["einstellung"] = nutzer_input.einstellung.__dict__

        nutzer_model: Final = NutzerModel.model_validate(nutzer_dict)
        nutzer_dto: Final = _write_service.create(nutzer=nutzer_model.to_nutzer())
        payload: Final = CreatePayload(id=nutzer_dto.id)  # pyright: ignore[reportArgumentType]

        logger.debug("{}", payload)
        return payload
