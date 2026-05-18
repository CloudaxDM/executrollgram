# Executrollgram

Bot de Telegram para ejecutar scripts desde comandos como `/backup` usando Docker Compose.

La imagen `ghcr.io/cloudaxdm/executrollgram:latest` está publicada para `linux/amd64` y `linux/arm64`.

## compose.yaml

```yaml
services:
  executrollgram:
    image: ghcr.io/cloudaxdm/executrollgram:latest
    environment:
      BOT_TOKEN: "tu_token_de_telegram"
      SCRIPTS_DIR: /app/scripts
      ALLOWED_CHAT_IDS: "tu_chat_id"
      SCRIPT_TIMEOUT_SECONDS: "60"
      MAX_OUTPUT_CHARS: "3500"
    volumes:
      - ./scripts:/app/scripts:ro
    restart: unless-stopped
```

## Scripts

Monta tus scripts en la carpeta local `./scripts`.

```text
scripts/backup.sh  ->  /backup
scripts/restart    ->  /restart
```

No hay que dar de alta scripts en ningún fichero. Al copiar un script válido en `./scripts`, el bot lo detecta.

Nombres válidos: letras, números, `_` y `-`. En Telegram no escribas `.sh`.
