# Telegram Script Bot Tasks

## Task 1: Bootstrap Python App
- Status: Done (`python -m compileall telegram_script_bot` passed).
- Objective: Crear estructura mínima del proyecto, dependencias y configuración de ejemplo.
- Expected files touched: `pyproject.toml`, `.env.example`, `README.md`, `telegram_script_bot/__init__.py`, `telegram_script_bot/__main__.py`, `telegram_script_bot/config.py`, `scripts/.gitkeep`.
- Expected result: El proyecto tiene paquete importable y configuración local documentada.
- Acceptance criteria: AC1.
- Validation command: `python -m compileall telegram_script_bot`.

## Task 2: Script Discovery And Execution
- Status: Done (`python -m compileall telegram_script_bot` passed).
- Objective: Implementar listado, validación y ejecución segura de scripts.
- Expected files touched: `telegram_script_bot/scripts.py`, `telegram_script_bot/__main__.py`, `README.md`.
- Expected result: Se pueden listar scripts y ejecutar uno por nombre validado.
- Acceptance criteria: AC2, AC3, AC5, AC6.
- Validation command: `python -m compileall telegram_script_bot`.

## Task 3: Telegram Bot Handlers
- Status: Done (`python -m compileall telegram_script_bot` passed).
- Objective: Conectar Telegram con `/start`, `/help` y comandos dinámicos.
- Expected files touched: `telegram_script_bot/bot.py`, `telegram_script_bot/__main__.py`, `README.md`.
- Expected result: El bot arranca por polling y responde comandos.
- Acceptance criteria: AC2, AC3.
- Validation command: `python -m compileall telegram_script_bot`.

## Task 4: Authorization And Error Responses
- Status: Done (`python -m compileall telegram_script_bot` passed).
- Objective: Aplicar `ALLOWED_CHAT_IDS` y mensajes claros ante errores.
- Expected files touched: `telegram_script_bot/bot.py`, `telegram_script_bot/scripts.py`, `README.md`.
- Expected result: Chats no permitidos no ejecutan scripts y los errores son seguros.
- Acceptance criteria: AC4, AC5, AC6.
- Validation command: `python -m compileall telegram_script_bot`.

## Task 5: Local Environment Validation
- Status: Done (`.venv\\Scripts\\python -m compileall telegram_script_bot` and `.venv\\Scripts\\telegram-script-bot --list` passed).
- Objective: Crear/usar `.venv`, instalar dependencias y validar arranque sin token real.
- Expected files touched: `requirements.txt` or lock files if chosen by tooling.
- Expected result: Entorno local reproducible.
- Acceptance criteria: AC1.
- Validation command: `.venv\\Scripts\\python -m compileall telegram_script_bot`.

## Task 6: Docker Runtime
- Status: Done (`.venv\\Scripts\\python -m compileall telegram_script_bot` passed; Docker build could not run because `docker` is not installed/available in this environment).
- Objective: Empaquetar la app para Docker con carpeta `scripts/` mapeable como volumen.
- Expected files touched: `Dockerfile`, `.dockerignore`, `compose.yaml`, `README.md`.
- Expected result: Se puede ejecutar el bot con `docker compose` usando variables en `environment` y modificar scripts sin reconstruir imagen.
- Acceptance criteria: AC1, AC7.
- Validation command: `docker build -t telegram-script-bot .`.

## Task 7: GitHub Container Publishing
- Status: Done (workflow syntax added; Docker/GitHub Actions execution must run on GitHub).
- Objective: Publicar la imagen automáticamente desde GitHub para que otros puedan descargarla con `docker pull` y reconstruirla mensualmente con la imagen base actualizada.
- Expected files touched: `.github/workflows/docker-publish.yml`, `README.md`, `docs/decisions.md`.
- Expected result: Push a `main` publica `ghcr.io/USUARIO/REPOSITORIO:latest`; tags `v*` publican versiones; el schedule mensual reconstruye usando `pull: true`.
- Acceptance criteria: AC7.
- Validation command: GitHub Actions run `Publish Docker Image`.

## Task 8: Telegram Command Menu Refresh
- Status: Done (`.venv\\Scripts\\python -m compileall telegram_script_bot` passed).
- Objective: Registrar comandos nativos de Telegram, refrescarlos periódicamente y permitir refresco manual con `/reload`.
- Expected files touched: `telegram_script_bot/bot.py`, `telegram_script_bot/config.py`, `telegram_script_bot/scripts.py`, `compose.yaml`, `README.md`, `docs/decisions.md`.
- Expected result: El menú de Telegram incluye `/help`, `/reload` y scripts compatibles con Bot API; las descripciones salen del primer comentario útil del script.
- Acceptance criteria: AC2, AC3, AC7.
- Validation command: `.venv\\Scripts\\python -m compileall telegram_script_bot`.
