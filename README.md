# Executrollgram

Bot de Telegram para ejecutar scripts desde comandos como `/backup` usando Docker Compose.

La imagen `ghcr.io/cloudaxdm/executrollgram:latest` está publicada para `linux/amd64` y `linux/arm64`.

## compose.yaml

```yaml
services:
  executrollgram:
    image: ghcr.io/cloudaxdm/executrollgram:latest
    environment:
      # Token del bot de Telegram creado con BotFather.
      BOT_TOKEN: "tu_token_de_telegram"
      # Ruta interna donde el contenedor ve los scripts montados.
      SCRIPTS_DIR: /app/scripts
      # Chat IDs permitidos, separados por coma. Obligatorio en producción.
      ALLOWED_CHAT_IDS: "tu_chat_id"
      # Pon "true" solo la primera vez para que el bot te diga tu chat_id si no estás autorizado. Luego vuelve a "false".
      REVEAL_CHAT_ID_ON_DENY: "true"
      # Tiempo máximo de ejecución por script, en segundos.
      SCRIPT_TIMEOUT_SECONDS: "60"
      # Máximo de caracteres devueltos a Telegram por ejecución.
      MAX_OUTPUT_CHARS: "3500"
    volumes:
      - ./scripts:/app/scripts:ro
    restart: unless-stopped
```

La primera vez deja `REVEAL_CHAT_ID_ON_DENY: "true"`, copia el `chat_id` que devuelve el bot si responde `No autorizado`, ponlo en `ALLOWED_CHAT_IDS` y cambia `REVEAL_CHAT_ID_ON_DENY` a `"false"`.

## Scripts

Monta tus scripts en la carpeta local `./scripts`.

```text
scripts/backup.sh  ->  /backup
scripts/restart    ->  /restart
```

No hay que dar de alta scripts en ningún fichero. Al copiar un script válido en `./scripts`, el bot lo detecta.

Nombres válidos: letras, números, `_` y `-`. En Telegram no escribas `.sh`.
