# Executrollgram

Bot de Telegram para ejecutar scripts locales desde comandos como `/backup`.

## Docker Compose

Crea el archivo `.env`:

```env
BOT_TOKEN=tu_token_de_telegram
SCRIPTS_DIR=/app/scripts
ALLOWED_CHAT_IDS=tu_chat_id
SCRIPT_TIMEOUT_SECONDS=60
MAX_OUTPUT_CHARS=3500
```

Crea la carpeta de scripts:

```bash
mkdir -p scripts
```

Ejemplo de script:

```bash
cat > scripts/backup.sh <<'EOF'
#!/usr/bin/env bash
echo "Backup ejecutado"
date
EOF
chmod +x scripts/backup.sh
```

Arranca el contenedor:

```bash
docker compose up -d
```

Ver logs:

```bash
docker compose logs -f
```

Parar:

```bash
docker compose down
```

## Montaje De Scripts

El `compose.yaml` monta la carpeta local `./scripts` dentro del contenedor:

```yaml
volumes:
  - ./scripts:/app/scripts:ro
```

Por eso solo tienes que copiar scripts a `./scripts`. No hace falta reconstruir la imagen.

Ejemplos:

```text
scripts/backup.sh  ->  /backup
scripts/restart    ->  /restart
```

Los nombres válidos solo pueden usar letras, números, `_` y `-`. En Telegram no escribas `.sh`.

## Imagen Publicada

```bash
docker pull ghcr.io/cloudaxdm/executrollgram:latest
```

Si prefieres usar la imagen publicada en vez de construir localmente, cambia `compose.yaml` para usar:

```yaml
services:
  telegram-script-bot:
    image: ghcr.io/cloudaxdm/executrollgram:latest
    env_file:
      - .env
    environment:
      SCRIPTS_DIR: /app/scripts
    volumes:
      - ./scripts:/app/scripts:ro
    restart: unless-stopped
```
