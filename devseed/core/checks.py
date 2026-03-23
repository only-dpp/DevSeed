import sys
from pathlib import Path

from devseed.core.files import dir_exists, file_exists
from devseed.core.shell import command_exists


def check_python() -> bool:
    return sys.version_info >= (3, 10)


def check_pip() -> bool:
    return command_exists("pip")


def check_git() -> bool:
    return command_exists("git")


def check_project_structure(base_path: Path) -> dict[str, bool]:
    return {
        "app_dir": dir_exists(base_path / "app"),
        "requirements": file_exists(base_path / "requirements.txt"),
        "env_example": file_exists(base_path / ".env.example"),
        "main_file": file_exists(base_path / "app" / "main.py"),
    }


def check_venv(base_path: Path) -> bool:
    return dir_exists(base_path / ".venv")


def check_env_file(base_path: Path) -> bool:
    return file_exists(base_path / ".env")