from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import Config

SCRIPT_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")


class ScriptError(Exception):
    """Raised when a script cannot be safely executed."""


@dataclass(frozen=True)
class ScriptResult:
    name: str
    returncode: int
    output: str
    timed_out: bool = False


def list_scripts(config: Config) -> list[str]:
    if not config.scripts_dir.is_dir():
        return []

    scripts: list[str] = []
    for path in config.scripts_dir.iterdir():
        if not path.is_file():
            continue
        if is_valid_script_name(path.name):
            scripts.append(path.name)
        elif path.suffix == ".sh" and is_valid_script_name(path.stem):
            scripts.append(path.stem)
    return sorted(set(scripts))


def run_script(config: Config, name: str) -> ScriptResult:
    if not is_valid_script_name(name):
        raise ScriptError("Invalid script name.")

    script_path = _find_script_path(config.scripts_dir, name)
    if not script_path.is_file():
        raise ScriptError("Script not found.")

    command = [os.fspath(script_path)]
    if script_path.suffix == ".sh":
        command = ["bash", os.fspath(script_path)]

    try:
        completed = subprocess.run(
            command,
            cwd=os.fspath(config.scripts_dir),
            capture_output=True,
            text=True,
            timeout=config.script_timeout_seconds,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        output = _join_output(exc.stdout, exc.stderr) or "Script timed out."
        return ScriptResult(name=name, returncode=124, output=_limit_output(output, config), timed_out=True)
    except OSError as exc:
        raise ScriptError(f"Could not execute script: {exc}") from exc

    output = _join_output(completed.stdout, completed.stderr)
    if not output:
        output = f"Script finished with exit code {completed.returncode}."
    return ScriptResult(name=name, returncode=completed.returncode, output=_limit_output(output, config))


def is_valid_script_name(name: str) -> bool:
    return bool(SCRIPT_NAME_RE.fullmatch(name))


def _resolve_script_path(scripts_dir: Path, name: str) -> Path:
    base = scripts_dir.resolve()
    candidate = (base / name).resolve()
    if candidate.parent != base:
        raise ScriptError("Script path escapes scripts directory.")
    return candidate


def _find_script_path(scripts_dir: Path, name: str) -> Path:
    direct = _resolve_script_path(scripts_dir, name)
    if direct.is_file():
        return direct
    return _resolve_script_path(scripts_dir, f"{name}.sh")


def _join_output(stdout: str | bytes | None, stderr: str | bytes | None) -> str:
    parts = [_to_text(stdout).strip(), _to_text(stderr).strip()]
    return "\n".join(part for part in parts if part)


def _to_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value


def _limit_output(output: str, config: Config) -> str:
    if len(output) <= config.max_output_chars:
        return output
    suffix = "\n...[output truncated]"
    limit = max(config.max_output_chars - len(suffix), 0)
    return output[:limit] + suffix
