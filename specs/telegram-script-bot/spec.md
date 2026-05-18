# Telegram Script Bot Spec

## Problem
Se necesita una app Python sencilla que permita ejecutar scripts bash locales desde Telegram usando comandos como `/nombrescript` y devolver la salida al chat.

## Goal
Crear un bot configurable con token, usuarios permitidos y ruta de scripts, donde dar de alta scripts sea tan simple como dejar un archivo ejecutable en esa ruta.

## Non-goals
- No crear interfaz web.
- No editar scripts desde Telegram.
- No ejecutar comandos arbitrarios escritos por el usuario.
- No gestionar colas distribuidas ni ejecución remota.

## User Flows
- El administrador configura `BOT_TOKEN`, `SCRIPTS_DIR` y usuarios permitidos.
- El usuario escribe `/start` o `/help` y ve los scripts disponibles.
- El usuario escribe `/nombrescript` y el bot ejecuta `nombrescript` o `nombrescript.sh` dentro de `SCRIPTS_DIR`.
- El bot responde con salida estándar, error estándar y código de salida cuando corresponda.

## UI Requirements
- Respuestas en Telegram en texto plano.
- Listado claro de comandos disponibles.
- Salida recortada si supera el límite seguro de mensaje.

## State Requirements
- Sin estado persistente inicial.
- La lista de scripts se calcula leyendo la carpeta configurada.

## Backend/API Requirements
- Usar polling de Telegram para simplicidad local.
- Mapear cada comando `/nombre` a un script local con el mismo nombre.
- Ejecutar scripts con timeout configurable.
- Permitir ejecución en Docker con la carpeta de scripts montada como volumen.

## Data/Model Requirements
- Configuración por variables de entorno o archivo `.env` local.
- Scripts dados de alta como archivos sin extensión o `.sh` dentro de `SCRIPTS_DIR`.

## Validation Rules
- Solo ejecutar nombres de script seguros: letras, números, guion y guion bajo.
- No permitir rutas relativas, barras ni extensiones enviadas por Telegram.
- Solo ejecutar archivos existentes dentro de `SCRIPTS_DIR`.
- Restringir acceso a `ALLOWED_CHAT_IDS` si está configurado.

## Error States
- Token no configurado.
- Carpeta de scripts inexistente.
- Script no encontrado.
- Usuario no autorizado.
- Timeout de ejecución.
- Script devuelve error.

## Permissions/Security
- No ejecutar entrada arbitraria.
- Ejecutar siempre con `shell=False`.
- Recomendar permisos mínimos en scripts y carpeta.
- No incluir token real en el repositorio.

## Acceptance Criteria
- AC1: La app arranca con configuración desde entorno/.env.
- AC2: `/help` lista scripts disponibles.
- AC3: `/nombrescript` ejecuta solo el script permitido y devuelve salida.
- AC4: Un usuario no permitido recibe rechazo si `ALLOWED_CHAT_IDS` está configurado.
- AC5: Scripts inexistentes o nombres inválidos no se ejecutan.
- AC6: La ejecución tiene timeout y salida limitada.
- AC7: La app puede ejecutarse en Docker mapeando una carpeta local de scripts.

## Assumptions
- Se usará Python 3.10+ en `.venv`.
- Los scripts son bash o ejecutables compatibles con el sistema donde corra la app.
- El bot ya existe en Telegram y el usuario aportará el token real localmente.
