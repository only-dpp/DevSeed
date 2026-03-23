from pathlib import Path

from devseed.core.console import abort
from devseed.core.env import get_venv_python
from devseed.core.checks import check_project_structure


def is_valid_project(base_path: Path) -> bool:
    structure = check_project_structure(base_path)
    return all(structure.values())


def ensure_valid_project(base_path: Path) -> None:
    if not is_valid_project(base_path):
        abort(
            "Diretório atual não é um projeto válido do DevSeed.\n"
            "Verifique se você está na raiz de um projeto criado com o DevSeed."
        )


def ensure_project_with_venv(base_path: Path) -> Path:
    ensure_valid_project(base_path)

    python_path = get_venv_python(base_path)
    if not python_path.exists():
        abort(
            "Ambiente virtual não encontrado.\n"
            "Execute: python -m devseed setup"
        )

    return python_path