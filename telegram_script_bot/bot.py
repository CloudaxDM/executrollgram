from __future__ import annotations

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from .config import Config
from .scripts import ScriptError, list_scripts, run_script


def run_bot(config: Config) -> None:
    if not config.bot_token:
        raise SystemExit("BOT_TOKEN is required. Copy .env.example to .env and set it.")

    application = Application.builder().token(config.bot_token).build()

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if not _is_allowed(config, update):
            await _reply(update, "No autorizado.")
            return
        scripts = list_scripts(config)
        if not scripts:
            await _reply(update, "No hay scripts disponibles.")
            return
        commands = "\n".join(f"/{name}" for name in scripts)
        await _reply(update, f"Scripts disponibles:\n{commands}")

    async def script_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message
        if message is None or not message.text:
            return
        if not _is_allowed(config, update):
            await _reply(update, "No autorizado.")
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
    application.add_handler(MessageHandler(filters.COMMAND, script_command))
    application.run_polling()


def _is_allowed(config: Config, update: Update) -> bool:
    if not config.allowed_chat_ids:
        return True
    chat = update.effective_chat
    return chat is not None and chat.id in config.allowed_chat_ids


async def _reply(update: Update, text: str) -> None:
    message = update.effective_message
    if message is not None:
        await message.reply_text(text)
