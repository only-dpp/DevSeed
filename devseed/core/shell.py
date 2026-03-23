import subprocess
from pathlib import Path
from typing import Sequence


def run_command(
    command: Sequence[str],
    cwd: Path | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        text=True,
        capture_output=True,
    )


def command_exists(command_name: str) -> bool:
    result = subprocess.run(
        [command_name, "--version"],
        text=True,
        capture_output=True,
    )
    return result.returncode == 0