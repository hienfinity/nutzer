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

@nutzer_router.get(
    "/{nutzer_id}",
    # dependencies=[Depends(RolesRequired([Role.ADMIN, Role.NUTZER]))],
)
def get_by_id(
    nutzer_id: int,
    request: Request,
    service: Annotated[NutzerService, Depends(get_service)],
) -> Response:
    """Suche mit der Nutzer-ID.

    :param nutzer_id: ID des gesuchten Nutzers als Pfadparameter
    :param request: Injiziertes Request-Objekt mit ggf. If-None-Match im Header
    :param service: Injizierter Service fuer Geschaeftslogik
    :return: Response mit dem gefundenen Nutzerdatensatz
    :rtype: Response
    """
    # Spaeter aktivieren, sobald Security komplett eingebunden ist:
    # user: Final[User] = request.state.current_user
    logger.debug("nutzer_id={}", nutzer_id)

    nutzer: Final = service.find_by_id(nutzer_id=nutzer_id)
    logger.debug("{}", nutzer)

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]
        logger.debug("version={}", version)
        try:
            if int(version) == nutzer.version:
                return Response(status_code=status.HTTP_304_NOT_MODIFIED)
        except ValueError:
            logger.debug("invalid version={}", version)

    return JSONResponse(
        content=_nutzer_to_dict(nutzer),
        headers={ETAG: f'"{nutzer.version}"'},
    )
