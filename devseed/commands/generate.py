from pathlib import Path

import typer

from devseed.core.console import abort, console, section, success, title
from devseed.core.files import ensure_directory, write_file
from devseed.core.project import is_valid_project

app = typer.Typer(help="Gera estruturas básicas de código.")


def normalize_name(name: str) -> str:
    return name.strip().lower().replace("-", "_").replace(" ", "_")


def create_module(base_path: Path, module_name: str) -> None:
    module_name = normalize_name(module_name)

    module_path = base_path / "app" / module_name

    if module_path.exists():
        abort(f'O módulo "{module_name}" já existe.')

    ensure_directory(module_path)

    write_file(module_path / "__init__.py", "")

    write_file(
        module_path / "routes.py",
        f"""from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_{module_name}():
    return {{"module": "{module_name}"}}
""",
    )

    write_file(
        module_path / "service.py",
        "# business logic goes here\n",
    )

    write_file(
        module_path / "schemas.py",
        "# pydantic schemas go here\n",
    )


@app.command("module")
def generate_module(name: str) -> None:
    base_path = Path.cwd()

    title("DevSeed Generate")
    section("Gerando módulo")

    if not is_valid_project(base_path):
        abort("Diretório atual não é um projeto válido do DevSeed.")

    create_module(base_path, name)

    success(f'Módulo "{name}" criado com sucesso.')

    console.print()
    console.print("[bold]Próximo passo sugerido:[/]")
    console.print("[cyan]Registrar o router no app/main.py[/]")