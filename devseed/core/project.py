from pathlib import Path

from devseed.core.checks import check_project_structure


def is_valid_project(base_path: Path) -> bool:
    structure = check_project_structure(base_path)
    return all(structure.values())