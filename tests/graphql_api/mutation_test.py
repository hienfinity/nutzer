"""Tests fuer Mutations mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url
from httpx import post
from pytest import mark
