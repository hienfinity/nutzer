"""Router-Paket fuer die REST-Schnittstelle von Nutzer."""

from .adresse_model import AdresseModel
from .constants import (
    ETAG,
    IF_MATCH,
    IF_MATCH_MIN_LEN,
    IF_NONE_MATCH,
    IF_NONE_MATCH_MIN_LEN,
)
from .dependencies import get_repository, get_service, get_write_service
from .einstellung_model import EinstellungModel
from .nutzer_model import NutzerModel
from .nutzer_router import nutzer_router
from .nutzer_update_model import NutzerUpdateModel
from .nutzer_write_router import nutzer_write_router
from .page import Page

__all__ = [
    "ETAG",
    "IF_MATCH",
    "IF_MATCH_MIN_LEN",
    "IF_NONE_MATCH",
    "IF_NONE_MATCH_MIN_LEN",
    "AdresseModel",
    "EinstellungModel",
    "NutzerModel",
    "NutzerUpdateModel",
    "Page",
    "get_repository",
    "get_service",
    "get_write_service",
    "nutzer_router",
    "nutzer_write_router",
]
