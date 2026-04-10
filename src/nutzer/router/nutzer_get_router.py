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

@nutzer_router.get(
    "",
    # dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get(
    request: Request,
    service: Annotated[NutzerService, Depends(get_service)],
) -> JSONResponse:
    """Suche mit Query-Parametern.

    :param request: Injiziertes Request-Objekt mit Query-Parametern
    :param service: Injizierter Service fuer Geschaeftslogik
    :return: Response mit einer Seite mit Nutzerdaten
    :rtype: JSONResponse
    """
    query_params: Final = request.query_params
    log_str: Final = "{}"
    logger.debug(log_str, query_params)

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    suchparameter = dict(query_params)
    if "page" in query_params:
        del suchparameter["page"]
    if "size" in query_params:
        del suchparameter["size"]

    nutzer_slice: Final = service.find(
        suchparameter=suchparameter,
        pageable=pageable,
    )

    result: Final = _nutzer_slice_to_page(nutzer_slice, pageable)
    logger.debug(log_str, result)
    return JSONResponse(content=result)

@nutzer_router.get(
    "/nachnamen/{teil}",
    # dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get_nachnamen(
    teil: str,
    service: Annotated[NutzerService, Depends(get_service)],
) -> JSONResponse:
    """Suche Nachnamen zum gegebenen Teilstring.

    :param teil: Teilstring der gefundenen Nachnamen
    :param service: Injizierter Service fuer Geschaeftslogik
    :return: Response mit Statuscode 200 und gefundenen Nachnamen im Body
    :rtype: JSONResponse
    """
    logger.debug("teil={}", teil)
    nachnamen: Final = service.find_nachnamen(teil=teil)
    return JSONResponse(content=nachnamen)

def _nutzer_slice_to_page(
    nutzer_slice: Slice[NutzerDTO],
    pageable: Pageable,
) -> dict[str, Any]:
    nutzer_dict: Final = tuple(
        _nutzer_to_dict(nutzer) for nutzer in nutzer_slice.content
    )
    page: Final = Page.create(
        content=nutzer_dict,
        pageable=pageable,
        total_elements=nutzer_slice.total_elements,
    )
    return asdict(obj=page)
