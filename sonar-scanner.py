# Copyright (C) 2022 - present, Juergen Zimmermann, Hochschule Karlsruhe
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

# Aufruf:   python sonar-scanner.py

"""Python-Script, um den Scanner für SonarQube aufzurufen."""

import subprocess
from pathlib import Path
from sysconfig import get_platform

betriebssystem = get_platform()
base_path = (
    (Path("C:\\") / "Zimmermann")
    if betriebssystem in {"win-amd64", "win-arm64", "win32"}
    else Path("Zimmermann")
)
scanner_dateiname = "sonar-scanner.bat" if betriebssystem in {"win-amd64", "win-arm64", "win32"} else "sonar-scanner"


def ermittle_scanner_pfad(basis: Path) -> Path:
    direkter_pfad = basis / "sonar-scanner" / "bin" / scanner_dateiname
    if direkter_pfad.exists():
        return direkter_pfad

    kandidaten = sorted(basis.glob("sonar-scanner-*"))
    for kandidat in kandidaten:
        scanner = kandidat / "bin" / scanner_dateiname
        if scanner.exists():
            return scanner

    native_kandidaten = sorted(
        (Path.home() / ".sonar" / "native-sonar-scanner").glob(f"sonar-scanner-*/bin/{scanner_dateiname}")
    )
    if native_kandidaten:
        return native_kandidaten[-1]

    return direkter_pfad


script = ermittle_scanner_pfad(base_path)

if __name__ == "__main__":
    subprocess.run(f"{script} -X", shell=True)  # noqa: PLW1510
