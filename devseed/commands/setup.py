from pathlib import Path
import sys
import venv

import typer
from rich.console import Group
from rich.panel import Panel

from devseed.core.console import abort, console, section, success, title, warning
from devseed.core.env import get_venv_pip, get_venv_python
from devseed.core.files import copy_file_if_missing, file_exists
from devseed.core.project import is_valid_project
from devseed.core.shell import run_command

app = typer.Typer(help="Prepara o ambiente local do projeto.")


def create_virtualenv(base_path: Path) -> bool:
    venv_path = base_path / ".venv"

    if venv_path.exists():
        return False

    builder = venv.EnvBuilder(with_pip=True)
    builder.create(venv_path)
    return True


def install_dependencies(base_path: Path) -> None:
    requirements_file = base_path / "requirements.txt"

    if not file_exists(requirements_file):
        abort("requirements.txt not found in the current directory.")

    pip_path = get_venv_pip(base_path)

    if not pip_path.exists():
        abort("Could not find pip inside .venv.")

    result = run_command(
        [str(pip_path), "install", "-r", str(requirements_file)],
        cwd=base_path,
    )

    if result.returncode != 0:
        error_output = result.stderr.strip() or result.stdout.strip() or "Unknown pip error."
        abort(f"Failed to install dependencies.\n{error_output}")


def ensure_env_file(base_path: Path) -> bool:
    env_example = base_path / ".env.example"
    env_file = base_path / ".env"

    if not file_exists(env_example):
        abort(".env.example not found in the current directory.")

    return copy_file_if_missing(env_example, env_file)


@app.callback(invoke_without_command=True)
def setup() -> None:
    base_path = Path.cwd()

    title("DevSeed Setup")

    if not is_valid_project(base_path):
        abort("Current directory is not a valid DevSeed project.")

    section("Preparing environment")

    created_venv = create_virtualenv(base_path)
    if created_venv:
        success("Virtual environment created.")
    else:
        warning("Virtual environment already exists. Skipping creation.")

    install_dependencies(base_path)
    success("Dependencies installed.")

    created_env = ensure_env_file(base_path)
    if created_env:
        success("Environment file created from .env.example.")
    else:
        warning(".env already exists. Skipping creation.")

    section("Summary")
    console.print("[bold green]Environment setup completed.[/]")
    console.print()
    console.print("[bold]Suggested next step:[/]")
    console.print("[cyan]python -m devseed run api[/]  → start the local API")