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
    # dependencies=[Depends(RolesRequired(Role.ADMIN))],
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
