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
