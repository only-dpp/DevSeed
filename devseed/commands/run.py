from pathlib import Path
import subprocess

import typer

from devseed.core.console import abort, console, next_step, section, title, warning
from devseed.core.files import dir_exists
from devseed.core.project import ensure_project_with_venv

app = typer.Typer(help="Executa tarefas comuns do projeto.")


@app.command("api")
def run_api() -> None:
    base_path = Path.cwd()

    title("DevSeed Run")
    section("Iniciando API")

    python_path = ensure_project_with_venv(base_path)

    console.print("[bold]Comando:[/]")
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
        warning("Execução da API interrompida pelo usuário.")
    except subprocess.CalledProcessError:
        abort("Falha ao iniciar a API.")

@app.command("tests")
def run_tests() -> None:
    base_path = Path.cwd()

    title("DevSeed Run")
    section("Executando testes")

    python_path = ensure_project_with_venv(base_path)

    if not dir_exists(base_path / "tests"):
        abort("Diretório tests/ não encontrado.")

    console.print("[bold]Comando:[/]")
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
        warning("Execução dos testes interrompida pelo usuário.")
    except subprocess.CalledProcessError:
        abort("Os testes falharam.")


@app.command("test")
def run_test_alias() -> None:
    run_tests()