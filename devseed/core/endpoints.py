from pathlib import Path

from devseed.core.files import file_exists

ALLOWED_HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def normalize_name(name: str) -> str:
    return name.strip().lower().replace("-", "_").replace(" ", "_")


def normalize_http_method(method: str) -> str:
    return method.strip().lower()


def is_valid_http_method(method: str) -> bool:
    return normalize_http_method(method) in ALLOWED_HTTP_METHODS


def build_endpoint_route_line(http_method: str, endpoint_name: str) -> str:
    return f'@router.{http_method}("/{endpoint_name}")'


def build_endpoint_function_name(module_name: str, endpoint_name: str, http_method: str) -> str:
    return f"{http_method}_{module_name}_{endpoint_name}"


def build_service_import(module_name: str, function_name: str) -> str:
    return f"from app.{module_name}.service import {function_name}"


def build_endpoint_function(module_name: str, endpoint_name: str, http_method: str) -> str:
    function_name = build_endpoint_function_name(module_name, endpoint_name, http_method)

    return f"""@router.{http_method}("/{endpoint_name}")
def {endpoint_name}():
    return {function_name}()
"""


def insert_import_if_missing(content: str, import_line: str) -> str:
    if import_line in content:
        return content

    lines = content.splitlines()

    insert_index = 0
    for index, line in enumerate(lines):
        if line.startswith("from ") or line.startswith("import "):
            insert_index = index + 1

    lines.insert(insert_index, import_line)
    return "\n".join(lines)


def append_endpoint_to_routes(
    base_path: Path,
    module_name: str,
    endpoint_name: str,
    http_method: str,
) -> bool:
    routes_file = base_path / "app" / module_name / "routes.py"

    if not file_exists(routes_file):
        raise FileNotFoundError(f'Arquivo de rotas não encontrado em app/{module_name}/routes.py.')

    content = routes_file.read_text(encoding="utf-8")

    route_line = build_endpoint_route_line(http_method, endpoint_name)
    function_name = build_endpoint_function_name(module_name, endpoint_name, http_method)

    if route_line in content or f"def {endpoint_name}():" in content:
        return False

    import_line = build_service_import(module_name, function_name)
    content = insert_import_if_missing(content, import_line)

    endpoint_block = build_endpoint_function(module_name, endpoint_name, http_method)

    new_content = content.rstrip() + "\n\n\n" + endpoint_block + "\n"
    routes_file.write_text(new_content, encoding="utf-8")

    return True