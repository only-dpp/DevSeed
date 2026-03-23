from pathlib import Path
import subprocess

import typer

from devseed.core.console import abort, console, section, title
from devseed.core.env import get_venv_python
from devseed.core.files import dir_exists
from devseed.core.project import is_valid_project

app = typer.Typer(help="Executa tarefas comuns do projeto.")


def ensure_ready_project(base_path: Path) -> Path:
    if not is_valid_project(base_path):
        abort("Current directory is not a valid DevSeed project.")

    python_path = get_venv_python(base_path)

    if not python_path.exists():
        abort("Virtual environment not found. Run 'python -m devseed setup' first.")

    return python_path


@app.command("api")
def run_api() -> None:
    base_path = Path.cwd()

    title("DevSeed Run")
    section("Starting API")

    python_path = ensure_ready_project(base_path)

    console.print("[bold]Command:[/]")
    console.print("[cyan]python -m uvicorn app.main:app --reload[/]")
    console.print()

    try:
        subprocess.run(
            [str(python_path), "-m", "uvicorn", "app.main:app", "--reload"],
            cwd=base_path,
            check=True,
        )
    except KeyboardInterrupt:
        console.print()
        console.print("[yellow]API execution interrupted by user.[/]")
    except subprocess.CalledProcessError:
        abort("Failed to start the API.")


@app.command("tests")
def run_tests() -> None:
    base_path = Path.cwd()

    title("DevSeed Run")
    section("Running tests")

    python_path = ensure_ready_project(base_path)

    if not dir_exists(base_path / "tests"):
        abort("tests/ directory not found.")

    console.print("[bold]Command:[/]")
    console.print("[cyan]python -m pytest[/]")
    console.print()

    try:
        subprocess.run(
            [str(python_path), "-m", "pytest"],
            cwd=base_path,
            check=True,
        )
    except KeyboardInterrupt:
        console.print()
        console.print("[yellow]Test execution interrupted by user.[/]")
    except subprocess.CalledProcessError:
        abort("Tests failed.")