"""Unit-Tests fuer find_by_id() von NutzerService."""

from dataclasses import asdict
from datetime import date
from typing import TYPE_CHECKING

from pytest import fixture, mark, raises

from nutzer.entity import Adresse, Einstellung, Interesse, Nutzer, Rolle, Status
from nutzer.service import NotFoundError, NutzerDTO, NutzerService

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
