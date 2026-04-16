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

__all__ = ["nutzer_write_router"]


nutzer_write_router: Final = APIRouter(tags=["Schreiben"])

@nutzer_write_router.post(
    "",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def post(
    nutzer_model: NutzerModel,
    request: Request,
    service: Annotated[NutzerWriteService, Depends(get_write_service)],
) -> Response:
    """POST-Request, um einen neuen Nutzer anzulegen.

    :param nutzer_model: Nutzerdaten als Pydantic-Model
    :param request: Injiziertes Request-Objekt mit der Request-URL
    :param service: Injizierter Service fuer Geschaeftslogik
    :rtype: Response
    :raises EmailExistsError: Falls die Emailadresse bereits existiert
    :raises UsernameExistsError: Falls der Benutzername bereits existiert
    """
    logger.debug("nutzer_model={}", nutzer_model)
    nutzer_dto: Final = service.create(nutzer=nutzer_model.to_nutzer())
    logger.debug("nutzer_dto={}", nutzer_dto)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{nutzer_dto.id}"},
    )

@nutzer_write_router.put(
    "/{nutzer_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.NUTZER]))],
)
def put(
    nutzer_id: int,
    nutzer_update_model: NutzerUpdateModel,
    request: Request,
    service: Annotated[NutzerWriteService, Depends(get_write_service)],
) -> Response:
    """PUT-Request, um einen Nutzer zu aktualisieren.

    :param nutzer_id: ID des zu aktualisierenden Nutzers als Pfadparameter
    :param request: Injiziertes Request-Objekt mit If-Match im Header
    :param service: Injizierter Service fuer Geschaeftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    :raises EmailExistsError: Falls die neue Emailadresse bereits existiert
    :raises UsernameExistsError: Falls der neue Benutzername bereits existiert
    :raises NotFoundError: Falls zur ID kein Nutzer existiert
    :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
    """
    if_match_value: Final = request.headers.get(IF_MATCH)
    logger.debug(
        "nutzer_id={}, if_match={}, nutzer_update_model={}",
        nutzer_id,
        if_match_value,
        nutzer_update_model,
    )

    if if_match_value is None:
        return create_problem_details(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
        )

    if (
        len(if_match_value) < IF_MATCH_MIN_LEN
        or not if_match_value.startswith('"')
        or not if_match_value.endswith('"')
    ):
        return create_problem_details(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    version: Final = if_match_value[1:-1]
    try:
        version_int: Final = int(version)
    except ValueError:
        return Response(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    nutzer: Final = nutzer_update_model.to_nutzer()
    nutzer_modified: Final = service.update(
        nutzer=nutzer,
        nutzer_id=nutzer_id,
        version=version_int,
    )
    logger.debug("nutzer_modified={}", nutzer_modified)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={ETAG: f'"{nutzer_modified.version}"'},
    )

@nutzer_write_router.delete(
    "/{nutzer_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.NUTZER]))],
)
def delete_by_id(
    nutzer_id: int,
    service: Annotated[NutzerWriteService, Depends(get_write_service)],
) -> Response:
    """DELETE-Request, um einen Nutzer anhand seiner ID zu loeschen.

    :param nutzer_id: ID des zu loeschenden Nutzers
    :param service: Injizierter Service fuer Geschaeftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    """
    logger.debug("nutzer_id={}", nutzer_id)
    service.delete_by_id(nutzer_id=nutzer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
