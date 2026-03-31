# Nutzer: Anfangszustand

Dieses Verzeichnis enthaelt den sauberen Startzustand fuer das Projekt `Nutzer`.

Enthalten sind nur die Dateien, die du fuer den Projektbeginn brauchst:

- minimales Python-/FastAPI-Grundgeruest
- Konfiguration unter `src/nutzer/config`
- Security-Grundgeruest unter `src/nutzer/security`
- Einstiegspunkt zum Starten der Anwendung

Noch nicht enthalten sind fachliche Schichten wie `entity`, `repository`, `service`,
`router` oder `graphql_api` fuer die neue Domaene. Diese sollen danach Schritt fuer
Schritt aufgebaut werden.

Starten:

```powershell
uv sync
uv run nutzer
```
