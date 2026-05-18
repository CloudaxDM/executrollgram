from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    bot_token: str
    scripts_dir: Path
    allowed_chat_ids: frozenset[int]
    script_timeout_seconds: int
    max_output_chars: int

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()

        token = os.getenv("BOT_TOKEN", "").strip()
        scripts_dir = Path(os.getenv("SCRIPTS_DIR", "./scripts")).expanduser().resolve()
        allowed_chat_ids = _parse_chat_ids(os.getenv("ALLOWED_CHAT_IDS", ""))
        timeout = _parse_positive_int("SCRIPT_TIMEOUT_SECONDS", default=60)
        max_output_chars = _parse_positive_int("MAX_OUTPUT_CHARS", default=3500)

        return cls(
            bot_token=token,
            scripts_dir=scripts_dir,
            allowed_chat_ids=allowed_chat_ids,
            script_timeout_seconds=timeout,
            max_output_chars=max_output_chars,
        )


def _parse_chat_ids(value: str) -> frozenset[int]:
    if not value.strip():
        return frozenset()

    chat_ids: set[int] = set()
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            chat_ids.add(int(item))
        except ValueError as exc:
            raise ValueError(f"Invalid chat id in ALLOWED_CHAT_IDS: {item!r}") from exc
    return frozenset(chat_ids)


def _parse_positive_int(name: str, default: int) -> int:
    value = os.getenv(name, str(default)).strip()
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return parsed
