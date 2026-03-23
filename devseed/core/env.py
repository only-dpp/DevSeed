from pathlib import Path


def get_venv_python(base_path: Path) -> Path:
    windows_python = base_path / ".venv" / "Scripts" / "python.exe"
    unix_python = base_path / ".venv" / "bin" / "python"

    if windows_python.exists():
        return windows_python

    return unix_python


def get_venv_pip(base_path: Path) -> Path:
    windows_pip = base_path / ".venv" / "Scripts" / "pip.exe"
    unix_pip = base_path / ".venv" / "bin" / "pip"

    if windows_pip.exists():
        return windows_pip

    return unix_pip