# Copyright (C) 2023 - present Juergen Zimmermann, Hochschule Karlsruhe
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

# https://docs.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands?view=powershell-7

# Aufruf:   uv run extras/dependency-check.py

"""Python-Script, um OWASP Dependency Check aufzurufen."""

import subprocess
from os import environ
from pathlib import Path
from sysconfig import get_platform

nvd_api_key = "47fbc0a4-9240-4fda-9a26-d7d5624c16bf"
project = "FastAPI"

base_script = "dependency-check"
betriebssystem = get_platform()
if betriebssystem in {"win-amd64", "win-arm64", "win32"}:
    base_exec_path = Path("C:/") / "Zimmermann"
    extension = "bat"
    base_script += ".bat"
    base_data_path = Path("C:\\") / "Zimmermann"
else:
    base_exec_path = Path("Zimmermann")
    base_data_path = Path("Zimmermann")

script = base_exec_path / "dependency-check" / "bin" / base_script
print(f"script={script}")

project_root = Path(__file__).resolve().parent.parent
data_path = base_data_path / "dependency-check-data"
scan_path = project_root
report_path = project_root / "extras"
suppression_path = project_root / "extras" / "suppression.xml"


def ermittle_java_pfad() -> Path | None:
    java_home = environ.get("JAVA_HOME")
    if java_home:
        java_path = Path(java_home) / "bin" / "java.exe"
        if java_path.exists():
            return java_path

    kandidaten = (
        Path("C:/Program Files/Java"),
        Path("C:/Program Files/Eclipse Adoptium"),
        Path.home() / ".sonar" / "cache",
        Path.home() / ".vscode" / "extensions",
        Path.home() / ".antigravity" / "extensions",
    )
    for basis in kandidaten:
        if not basis.exists():
            continue
        java_dateien = sorted(basis.rglob("java.exe"), reverse=True)
        if java_dateien:
            return java_dateien[0]

    return None


java_path = ermittle_java_pfad()
if java_path is None:
    msg = (
        "Keine Java-Laufzeit gefunden. "
        "Bitte JAVA_HOME setzen oder ein JDK/JRE installieren."
    )
    raise RuntimeError(msg)

options = " ".join([
    f'--nvdApiKey {nvd_api_key} --project {project} --scan "{scan_path}"',
    f'--suppression "{suppression_path}" --out "{report_path}" --data "{data_path}"',
    # dependency-check.bat --advancedHelp
    "--disableArchive",
    "--disableAssembly",
    "--disableAutoconf",
    "--disableBundleAudit",
    "--disableCarthageAnalyzer",
    "--disableCentral",
    "--disableCentralCache",
    "--disableCmake",
    "--disableCocoapodsAnalyzer",
    "--disableComposer",
    "--disableCpan",
    "--disableDart",
    "--disableGolangDep",
    "--disableGolangMod",
    "--disableJar",
    "--disableMavenInstall",
    "--disableMixAudit",
    "--disableMSBuild",
    "--disableNodeAudit",
    "--disableNodeAuditCache",
    "--disableNodeJS",
    "--disableNugetconf",
    "--disableNuspec",
    "--disableOssIndex",
    "--disablePipfile",
    "--disablePnpmAudit",
    "--disableRubygems",
    "--disableSwiftPackageManagerAnalyzer",
    "--disableSwiftPackageResolvedAnalyzer",
    "--disableYarnAudit",
])
print(f"options={options}")
print()

env = environ.copy()
env["JAVA_HOME"] = str(java_path.parent.parent)
env["PATH"] = f"{java_path.parent};{env.get('PATH', '')}"

subprocess.run(f'"{script}" {options}', shell=True, check=True, env=env)  # noqa: PLW1510
