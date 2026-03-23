from pathlib import Path

import typer

from devseed.core.codegen import register_router_in_main
from devseed.core.console import abort, console, next_step, section, success, title, warning
from devseed.core.files import ensure_directory, write_file
from devseed.core.project import is_valid_project

app = typer.Typer(help="Gera estruturas básicas de código.")


def normalize_name(name: str) -> str:
    return name.strip().lower().replace("-", "_").replace(" ", "_")


def create_module_files(base_path: Path, module_name: str) -> str:
    normalized_name = normalize_name(module_name)
    module_path = base_path / "app" / normalized_name

    if module_path.exists():
        abort(f'O módulo "{normalized_name}" já existe.')

    ensure_directory(module_path)

    write_file(module_path / "__init__.py", "")

    write_file(
        module_path / "routes.py",
        f"""from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_{normalized_name}():
    return {{"module": "{normalized_name}"}}
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

    return normalized_name


def create_module_test(base_path: Path, module_name: str) -> None:
    test_file = base_path / "tests" / f"test_{module_name}.py"

    write_file(
        test_file,
        f'''from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_{module_name}():
    response = client.get("/{module_name}")
    assert response.status_code == 200
    assert response.json() == {{"module": "{module_name}"}}
''',
    )


@app.command("module")
def generate_module(name: str) -> None:
    base_path = Path.cwd()

    title("DevSeed Generate")
    section("Gerando módulo")

    if not is_valid_project(base_path):
        abort(
            "Diretório atual não é um projeto válido do DevSeed.\n"
            "Verifique se você está na raiz de um projeto criado com o DevSeed."
        )

    module_name = create_module_files(base_path, name)
    success(f'Módulo "{module_name}" criado com sucesso.')

    try:
        registered = register_router_in_main(base_path, module_name)
    except FileNotFoundError as exc:
        warning(str(exc))
        registered = False
    except ValueError as exc:
        warning(str(exc))
        registered = False

    if registered:
        success(f'Router do módulo "{module_name}" registrado em app/main.py.')
    else:
        warning(f'O router do módulo "{module_name}" não foi registrado automaticamente.')

    try:
        create_module_test(base_path, module_name)
        success(f'Teste do módulo "{module_name}" criado com sucesso.')
    except FileExistsError:
        warning(f'O teste do módulo "{module_name}" já existe.')

    next_step("python -m devseed run test", "executar os testes do projeto")