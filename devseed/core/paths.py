from pathlib import Path


def cwd() -> Path:
    return Path.cwd()


def project_root(project_name: str) -> Path:
    return cwd() / project_name


def venv_python_path(base_path: Path) -> Path:
    if (base_path / ".venv" / "Scripts" / "python.exe").exists():
        return base_path / ".venv" / "Scripts" / "python.exe"

    return base_path / ".venv" / "bin" / "python"