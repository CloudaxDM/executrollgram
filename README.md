# Telegram Script Bot

Bot de Telegram sencillo para ejecutar scripts locales desde comandos como `/backup` y devolver la salida al chat.

## Características

- Alta de scripts solo copiando archivos a una carpeta.
- Comandos `/nombre` mapeados a `nombre` o `nombre.sh`.
- Ejecución segura con `shell=False`.
- Allowlist opcional por `ALLOWED_CHAT_IDS`.
- Timeout y recorte de salida para evitar respuestas enormes.
- Docker listo para montar `./scripts` como volumen.
- Publicación automática de imagen en GitHub Container Registry.

## Configuración

Copia el ejemplo y edita tus valores:

```powershell
copy .env.example .env
```

Variables principales:

```env
BOT_TOKEN=123456:replace_me
SCRIPTS_DIR=./scripts
ALLOWED_CHAT_IDS=123456789
SCRIPT_TIMEOUT_SECONDS=60
MAX_OUTPUT_CHARS=3500
```

Para Docker usa:

```env
SCRIPTS_DIR=/app/scripts
```

No subas `.env` a GitHub.

## Scripts

Para crear un comando, añade un archivo en `scripts/`:

```text
scripts/backup
scripts/backup.sh
```

Ambos se ejecutan desde Telegram con:

```text
/backup
```

Reglas del nombre:

- Solo letras, números, `_` y `-`.
- Sin espacios.
- Sin rutas.
- En Telegram no se escribe la extensión `.sh`.

Ejemplo de script Linux:

```bash
#!/usr/bin/env bash
echo "Backup iniciado"
date
```

Dale permisos de ejecución si lo ejecutas directamente:

```bash
chmod +x scripts/backup
```

Los archivos `.sh` se ejecutan con `bash`, incluido dentro de la imagen Docker.

## Ejecutar En Local

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -e .
.venv\Scripts\telegram-script-bot
```

Comandos útiles sin Telegram:

```powershell
.venv\Scripts\telegram-script-bot --list
.venv\Scripts\telegram-script-bot --run backup
```

## Ejecutar Con Docker Compose

Construyendo localmente:

```powershell
docker compose up -d --build
```

Ver logs:

```powershell
docker compose logs -f
```

Parar:

```powershell
docker compose down
```

La carpeta local `./scripts` se monta en `/app/scripts` dentro del contenedor. Puedes añadir o cambiar scripts sin reconstruir la imagen.

## Imagen Desde GitHub

Este repositorio incluye una GitHub Action en `.github/workflows/docker-publish.yml`.

Cuando subas cambios a `main`, GitHub construirá y publicará la imagen en GitHub Container Registry:

```text
ghcr.io/USUARIO/REPOSITORIO:latest
```

También publica tags si subes versiones como `v1.0.0`:

```text
ghcr.io/USUARIO/REPOSITORIO:v1.0.0
```

Para descargarla:

```bash
docker pull ghcr.io/USUARIO/REPOSITORIO:latest
```

Para ejecutarla:

```bash
docker run -d \
  --name telegram-script-bot \
  --env-file .env \
  -e SCRIPTS_DIR=/app/scripts \
  -v "$PWD/scripts:/app/scripts:ro" \
  --restart unless-stopped \
  ghcr.io/USUARIO/REPOSITORIO:latest
```

Sustituye `USUARIO/REPOSITORIO` por el nombre real de tu repositorio en GitHub, en minúsculas.

## Publicar La Imagen En GitHub

1. Sube el proyecto a GitHub.
2. Ve a `Actions` y comprueba que está habilitado.
3. Haz push a `main`.
4. Entra en `Packages` dentro del repositorio o perfil.
5. Si quieres que cualquiera pueda hacer `docker pull`, cambia la visibilidad del paquete a pública.

Para crear una versión:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Seguridad

- No pongas el token real en el repositorio.
- Configura `ALLOWED_CHAT_IDS` en producción.
- Monta `scripts/` como solo lectura en Docker.
- El bot solo ejecuta archivos dentro de `SCRIPTS_DIR`.
- No permite comandos arbitrarios ni rutas enviadas por Telegram.
