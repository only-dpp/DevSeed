from pathlib import Path

from devseed.core.files import file_exists

SCHEMA_METHODS = {"post", "put", "patch"}


def method_requires_schema(method: str) -> bool:
    return method in SCHEMA_METHODS


def build_schema_class_name(module_name: str, endpoint_name: str, method: str) -> str:
    return (
        f"{method.capitalize()}"
        f"{module_name.capitalize()}"
        f"{''.join(part.capitalize() for part in endpoint_name.split('_'))}"
        "Schema"
    )


def build_schema_class(module_name: str, endpoint_name: str, method: str) -> str:
    class_name = build_schema_class_name(module_name, endpoint_name, method)

    return f"""
class {class_name}(BaseModel):
    example_field: str
"""


def ensure_basemodel_import(content: str) -> str:
    import_line = "from pydantic import BaseModel"

    if import_line in content:
        return content

    lines = content.splitlines()

    insert_index = 0
    for index, line in enumerate(lines):
        if line.startswith("from ") or line.startswith("import "):
            insert_index = index + 1

    lines.insert(insert_index, import_line)
    return "\n".join(lines)


def append_schema_class(
    base_path: Path,
    module_name: str,
    endpoint_name: str,
    method: str,
) -> tuple[bool, str | None]:
    if not method_requires_schema(method):
        return False, None

    schemas_file = base_path / "app" / module_name / "schemas.py"

    if not file_exists(schemas_file):
        raise FileNotFoundError(f'Arquivo de schemas não encontrado em app/{module_name}/schemas.py.')

    content = schemas_file.read_text(encoding="utf-8")
    class_name = build_schema_class_name(module_name, endpoint_name, method)

    if f"class {class_name}(BaseModel):" in content:
        return False, class_name

    content = ensure_basemodel_import(content)
    schema_block = build_schema_class(module_name, endpoint_name, method)

    new_content = content.rstrip() + "\n\n" + schema_block.strip() + "\n"
    schemas_file.write_text(new_content, encoding="utf-8")

    return True, class_name