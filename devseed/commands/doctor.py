from pathlib import Path

import typer
from rich.table import Table

from devseed.core.checks import (
    check_env_file,
    check_git,
    check_pip,
    check_project_structure,
    check_python,
    check_venv,
)
from devseed.core.console import console, title, section

app = typer.Typer(help="Diagnostica o ambiente e o projeto.")


@app.callback(invoke_without_command=True)
def doctor() -> None:
    base_path: Path = Path.cwd()

    title("[bold cyan]DevSeed[/] [dim]• Doctor[/]")
    section("Environment checks")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Check", style="white")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")

    python_ok = check_python()
    pip_ok = check_pip()
    git_ok = check_git()

    structure = check_project_structure(base_path)
    structure_ok = all(structure.values())

    venv_ok = check_venv(base_path)
    env_ok = check_env_file(base_path)

    table.add_row(
        "Python",
        "[green]✔ OK[/]" if python_ok else "[yellow]⚠ WARN[/]",
        "Compatible version found" if python_ok else "Python not found or version < 3.10",
    )
    table.add_row(
        "pip",
        "[green]✔ OK[/]" if pip_ok else "[yellow]⚠ WARN[/]",
        "Available" if pip_ok else "Not found",
    )
    table.add_row(
        "Git",
        "[green]✔ OK[/]" if git_ok else "[yellow]⚠ WARN[/]",
        "Available" if git_ok else "Not found",
    )
    table.add_row(
        "Project structure",
        "[green]✔ OK[/]" if structure_ok else "[yellow]⚠ WARN[/]",
        "Valid project structure" if structure_ok else "Project structure is incomplete",
    )
    table.add_row(
        ".venv",
        "[green]✔ OK[/]" if venv_ok else "[yellow]⚠ WARN[/]",
        "Virtual environment found" if venv_ok else "Virtual environment not found",
    )
    table.add_row(
        ".env",
        "[green]✔ OK[/]" if env_ok else "[yellow]⚠ WARN[/]",
        "Environment file found" if env_ok else "Environment file not found",
    )

    console.print(table)

    if not structure_ok:
        section("Missing items")

        if not structure["app_dir"]:
            console.print("[yellow]•[/] Missing directory: [bold]app/[/]")
        if not structure["requirements"]:
            console.print("[yellow]•[/] Missing file: [bold]requirements.txt[/]")
        if not structure["env_example"]:
            console.print("[yellow]•[/] Missing file: [bold].env.example[/]")
        if not structure["main_file"]:
            console.print("[yellow]•[/] Missing file: [bold]app/main.py[/]")

    section("Summary")

    if all([python_ok, pip_ok, git_ok, structure_ok, venv_ok, env_ok]):
        console.print("[bold green]Everything looks ready to go.[/]")
    else:
        console.print("[bold yellow]Some items still need attention.[/]")
        console.print() 
        console.print("[bold]Suggested next step:[/]")
        console.print("[cyan]devseed setup[/] → prepare your environment")