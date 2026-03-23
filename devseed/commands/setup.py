from pathlib import Path
import venv

import typer

from devseed.core.console import abort, console, next_step, section, success, title, warning
from devseed.core.env import get_venv_pip
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
        abort("Arquivo requirements.txt não encontrado no diretório atual.")

    pip_path = get_venv_pip(base_path)

    if not pip_path.exists():
        abort("Não foi possível localizar o pip dentro da .venv.")

    result = run_command(
        [str(pip_path), "install", "-r", str(requirements_file)],
        cwd=base_path,
    )

    if result.returncode != 0:
        error_output = result.stderr.strip() or result.stdout.strip() or "Erro desconhecido ao instalar dependências."
        abort(f"Falha ao instalar dependências.\n{error_output}")


def ensure_env_file(base_path: Path) -> bool:
    env_example = base_path / ".env.example"
    env_file = base_path / ".env"

    if not file_exists(env_example):
        abort("Arquivo .env.example não encontrado no diretório atual.")

    return copy_file_if_missing(env_example, env_file)


@app.callback(invoke_without_command=True)
def setup() -> None:
    base_path = Path.cwd()

    title("DevSeed Setup")

    if not is_valid_project(base_path):
        abort(
            "Diretório atual não é um projeto válido do DevSeed.\n"
            "Verifique se você está na raiz de um projeto criado com o DevSeed."
        )

    section("Preparando ambiente")

    created_venv = create_virtualenv(base_path)
    if created_venv:
        success("Ambiente virtual criado.")
    else:
        warning("Ambiente virtual já existe.")

    install_dependencies(base_path)
    success("Dependências instaladas.")

    created_env = ensure_env_file(base_path)
    if created_env:
        success("Arquivo .env criado a partir de .env.example.")
    else:
        warning("Arquivo .env já existe.")

    section("Resumo")
    console.print("[bold green]Ambiente configurado com sucesso.[/]")
    next_step("python -m devseed run api", "iniciar a API local")