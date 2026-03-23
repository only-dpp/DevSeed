from pathlib import Path
import shutil


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {path}")

    path.write_text(content, encoding="utf-8")


def safe_write_file(path: Path, content: str) -> bool:
    if path.exists():
        return False

    path.write_text(content, encoding="utf-8")
    return True


def file_exists(path: Path) -> bool:
    return path.exists() and path.is_file()


def dir_exists(path: Path) -> bool:
    return path.exists() and path.is_dir()


def copy_file_if_missing(source: Path, destination: Path) -> bool:
    if destination.exists():
        return False

    shutil.copyfile(source, destination)
    return True