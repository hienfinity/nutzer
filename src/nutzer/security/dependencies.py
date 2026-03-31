# Copyright (C) 2025 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Factory-Funktionen für Dependency Injection."""

from nutzer.security.token_service import TokenService
from nutzer.security.user_service import UserService

_token_service: TokenService | None = None
_user_service: UserService | None = None


def get_token_service() -> TokenService:
    """Factory-Funktion für TokenService."""
    global _token_service
    if _token_service is None:
        _token_service = TokenService()
    return _token_service


def get_user_service() -> UserService:
    """Factory-Funktion für UserService."""
    global _user_service
    if _user_service is None:
        _user_service = UserService()
    return _user_service

