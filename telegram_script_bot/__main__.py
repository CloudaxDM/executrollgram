from __future__ import annotations

import argparse

from .config import Config
from .scripts import list_scripts, run_script


def main() -> None:
    config = Config.from_env()
    parser = argparse.ArgumentParser(description="Telegram script bot")
    parser.add_argument("--list", action="store_true", help="list available scripts")
    parser.add_argument("--run", metavar="SCRIPT", help="run a configured script by name")
    args = parser.parse_args()

    if args.list:
        scripts = list_scripts(config)
        print("\n".join(scripts) if scripts else "No scripts found.")
        return

    if args.run:
        result = run_script(config, args.run)
        print(result.output)
        raise SystemExit(result.returncode)

    if not config.bot_token:
        raise SystemExit("BOT_TOKEN is required. Copy .env.example to .env and set it.")
    from .bot import run_bot

    run_bot(config)


if __name__ == "__main__":
    main()
