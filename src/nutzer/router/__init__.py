"""
Router module for nutzer application.

This module contains all API route handlers and related models for user management.
"""

from .adresse_model import Adresse
from .constants import *
from .dependencies import *
from .einstellung_model import Einstellung
from .nurzer_router import router as nurzer_router
from .nutzer_get_router import router as nutzer_get_router
from .nutzer_model import Nutzer
from .nutzer_update_model import NutzerUpdate
from .nutzer_write_router import router as nutzer_write_router
from .page import Page

__all__ = [
    "Adresse",
    "Einstellung",
    "Nutzer",
    "NutzerUpdate",
    "Page",
    "nurzer_router",
    "nutzer_get_router",
    "nutzer_write_router",
]
