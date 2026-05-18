# Decisions

## Telegram Script Bot
- Use `python-telegram-bot` with polling for a simple local bot.
- Register scripts by filename in `SCRIPTS_DIR`; Telegram commands never provide paths.
- Execute scripts with `shell=False`, validated names, timeout, and optional chat allowlist.
- Limit setuptools package discovery to `telegram_script_bot*` so SDD folders like `specs/` are not treated as installable packages.
- Map `/nombre` to either `nombre` or `nombre.sh`; `.sh` files run through `bash` so bash scripts are easy to register while Telegram never sends extensions.
- Docker uses `/app/scripts` as `SCRIPTS_DIR` and maps the host `./scripts` folder as a volume so scripts can change without rebuilding the image.
- Publish Docker images to GitHub Container Registry (`ghcr.io`) with GitHub Actions because it works with the built-in `GITHUB_TOKEN` and avoids external Docker Hub secrets.
- Compose configuration keeps runtime options directly under `environment` instead of using `.env`, making single-file deployments simpler.
- GitHub Actions rebuilds monthly with `pull: true` so the published app image picks up updates from the Python base image.
- Use `python:3-slim` instead of `python:latest` or a fixed minor version so monthly rebuilds follow the supported Python 3 slim image without switching to a larger default image variant.
- Publish Docker images for both `linux/amd64` and `linux/arm64` so the same GHCR tag works on x86 servers and ARM devices.
- `REVEAL_CHAT_ID_ON_DENY` defaults to false so unauthorized responses do not leak chat IDs after initial setup; users can temporarily enable it to discover the correct Bot API chat id.
- Telegram native command menu is refreshed at startup, periodically by default, and manually with `/reload`; script descriptions come from the first useful `#` comment in each script.
