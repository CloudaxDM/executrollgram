from __future__ import annotations

import asyncio

from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from .config import Config
from .scripts import ScriptError, describe_script, is_valid_telegram_command, list_scripts, run_script


def run_bot(config: Config) -> None:
    if not config.bot_token:
        raise SystemExit("BOT_TOKEN is required.")

    async def post_init(application: Application) -> None:
        await refresh_command_menu(application, config)
        if config.command_menu_refresh_enabled:
            asyncio.create_task(_refresh_command_menu_periodically(application, config))

    application = Application.builder().token(config.bot_token).post_init(post_init).build()

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if not _is_allowed(config, update):
            await _reply(update, _unauthorized_message(config, update))
            return
        scripts = list_scripts(config)
        if not scripts:
            await _reply(update, "No hay scripts disponibles.")
            return
        commands = "\n".join(f"/{name}" for name in scripts)
        await _reply(update, f"Scripts disponibles:\n{commands}")

    async def reload_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not _is_allowed(config, update):
            await _reply(update, _unauthorized_message(config, update))
            return

        await refresh_command_menu(context.application, config)
        await _reply(update, "Menú de comandos recargado.")

    async def script_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message
        if message is None or not message.text:
            return
        if not _is_allowed(config, update):
            await _reply(update, _unauthorized_message(config, update))
            return

        command = message.text.split(maxsplit=1)[0].lstrip("/")
        command = command.split("@", maxsplit=1)[0]
        if command in {"start", "help"}:
            await help_command(update, context)
            return

        try:
            result = run_script(config, command)
        except ScriptError as exc:
            await _reply(update, str(exc))
            return

        status = "timeout" if result.timed_out else f"exit {result.returncode}"
        await _reply(update, f"[{command}: {status}]\n{result.output}")

    application.add_handler(CommandHandler(["start", "help"], help_command))
    application.add_handler(CommandHandler("reload", reload_command))
    application.add_handler(MessageHandler(filters.COMMAND, script_command))
    application.run_polling()


async def refresh_command_menu(application: Application, config: Config) -> None:
    commands = [
        BotCommand("help", "Lista scripts disponibles"),
        BotCommand("reload", "Recarga el menú de comandos"),
    ]
    for name in list_scripts(config):
        if not is_valid_telegram_command(name):
            continue
        commands.append(BotCommand(name, describe_script(config, name)))
        if len(commands) >= 100:
            break

    await application.bot.set_my_commands(commands)


async def _refresh_command_menu_periodically(application: Application, config: Config) -> None:
    while True:
        await asyncio.sleep(config.command_menu_refresh_seconds)
        await refresh_command_menu(application, config)


def _is_allowed(config: Config, update: Update) -> bool:
    if not config.allowed_chat_ids:
        return True
    chat = update.effective_chat
    return chat is not None and chat.id in config.allowed_chat_ids


def _unauthorized_message(config: Config, update: Update) -> str:
    if not config.reveal_chat_id_on_deny:
        return "No autorizado."

    chat = update.effective_chat
    if chat is None:
        return "No autorizado. No se pudo detectar el chat_id."
    return f"No autorizado. Añade este chat_id a ALLOWED_CHAT_IDS: {chat.id}"


async def _reply(update: Update, text: str) -> None:
    message = update.effective_message
    if message is not None:
        await message.reply_text(text)
