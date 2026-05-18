# Telegram Script Bot Design

## Current Context
El proyecto no tiene código Python ni entorno creado. Solo existe configuración de opencode. La feature puede arrancar como una app Python mínima.

## Files Affected
- `pyproject.toml`
- `README.md`
- `.env.example`
- `telegram_script_bot/__main__.py`
- `telegram_script_bot/config.py`
- `telegram_script_bot/scripts.py`
- `telegram_script_bot/bot.py`
- `scripts/`
- `Dockerfile`
- `.dockerignore`
- `compose.yaml`

## New Files
- Paquete `telegram_script_bot` para separar configuración, descubrimiento/ejecución de scripts y handlers del bot.
- `.env.example` sin secretos reales.

## Architecture Decisions
- Usar `python-telegram-bot` por simplicidad y soporte directo de polling async.
- Configuración por entorno y `.env` mediante `python-dotenv`.
- Alta de scripts por archivo: un script llamado `backup` o `backup.sh` se invoca con `/backup`.
- No se usa `shell=True`; se ejecuta el path resuelto con `subprocess.run`.
- Docker ejecuta la app como usuario no root y espera scripts montados en `/app/scripts`.

## UI/Component Design
- `/start` y `/help` muestran scripts disponibles.
- Comandos dinámicos se atienden con un handler general de comandos.
- Mensajes largos se recortan y se indica truncado.

## State Design
- Sin base de datos.
- Lista de scripts calculada al recibir `/help` o ejecutar comando.

## Backend/API Design
- `Config.from_env()` carga token, ruta, timeout, límite de salida y chats permitidos.
- `list_scripts(config)` devuelve nombres válidos disponibles.
- `run_script(config, name)` valida nombre, resuelve path dentro de `SCRIPTS_DIR`, ejecuta y devuelve resultado.
- `bot.py` conecta Telegram con esas funciones.

## Data/Model Changes
- No hay modelos persistentes.

## Risks
- Ejecutar scripts locales desde Telegram es sensible: la allowlist por chat y la validación de nombres son obligatorias.
- En Windows, los `.sh` requieren `bash` en `PATH` (Git Bash, WSL o similar); los archivos sin extensión se ejecutan directamente.

## Validation Strategy
- Validar sintaxis con `python -m compileall telegram_script_bot`.
- Validar configuración importando `Config`.
- Probar manualmente con `.venv` y token real fuera del repositorio.
- Validar imagen con `docker build -t telegram-script-bot .` cuando Docker esté disponible.
