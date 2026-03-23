from pathlib import Path

from devseed.core.files import file_exists


def normalize_name(name: str) -> str:
    return name.strip().lower().replace("-", "_").replace(" ", "_")


def build_endpoint_path(endpoint_name: str) -> str:
    return f'@router.get("/{endpoint_name}")'


def build_endpoint_function(module_name: str, endpoint_name: str) -> str:
    return f"""@router.get("/{endpoint_name}")
def get_{module_name}_{endpoint_name}():
    return {{"endpoint": "{endpoint_name}", "module": "{module_name}"}}
"""


def append_endpoint_to_routes(base_path: Path, module_name: str, endpoint_name: str) -> bool:
    routes_file = base_path / "app" / module_name / "routes.py"

    if not file_exists(routes_file):
        raise FileNotFoundError(f'Arquivo de rotas não encontrado em app/{module_name}/routes.py.')

    content = routes_file.read_text(encoding="utf-8")

    route_marker = build_endpoint_path(endpoint_name)
    function_name = f"def get_{module_name}_{endpoint_name}():"

    if route_marker in content or function_name in content:
        return False

    endpoint_block = build_endpoint_function(module_name, endpoint_name)

    new_content = content.rstrip() + "\n\n\n" + endpoint_block + "\n"
    routes_file.write_text(new_content, encoding="utf-8")

    return True