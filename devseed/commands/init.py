import typer
from pathlib import Path

from devseed.core.console import abort, console, plain, success, title
from devseed.core.files import ensure_directory, write_file
from devseed.core.paths import project_root
from devseed.templates.python_api import (
    ENV_EXAMPLE_TEMPLATE,
    GITIGNORE_TEMPLATE,
    MAIN_TEMPLATE,
    PYPROJECT_TEMPLATE,
    README_TEMPLATE,
    REQUIREMENTS_TEMPLATE,
)

app = typer.Typer(help="Cria a estrutura inicial de um projeto.")


def create_project_structure(base_path: Path, project_name: str) -> None:
    ensure_directory(base_path)
    ensure_directory(base_path / "app")
    ensure_directory(base_path / "tests")

    write_file(base_path / "app" / "__init__.py", "")
    write_file(base_path / "app" / "main.py", MAIN_TEMPLATE)
    write_file(base_path / "tests" / "__init__.py", "")

    write_file(base_path / ".env.example", ENV_EXAMPLE_TEMPLATE)
    write_file(base_path / ".gitignore", GITIGNORE_TEMPLATE)
    write_file(base_path / "requirements.txt", REQUIREMENTS_TEMPLATE)
    write_file(
        base_path / "README.md",
        README_TEMPLATE.format(project_name=project_name),
    )
    write_file(
        base_path / "pyproject.toml",
        PYPROJECT_TEMPLATE.format(project_name=project_name),
    )


@app.callback(invoke_without_command=True)
def init(project_name: str = typer.Argument(...)) -> None:
    base_path = project_root(project_name)

    title("DevSeed Init")

    if base_path.exists():
        abort(f'The directory "{project_name}" already exists.')

    console.print(f'Creating project [bold cyan]"{project_name}"[/]...')
    create_project_structure(base_path, project_name)

    success(f'Project "{project_name}" created successfully.')

    plain()
    console.print("[bold]Next steps:[/]")
    console.print(f"[cyan]cd[/] {project_name}")
    console.print("[cyan]devseed[/] doctor")
    console.print("[cyan]devseed[/] setup")
    console.print("[cyan]devseed[/] run api")