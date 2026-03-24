from pathlib import Path

from devseed.core.files import file_exists


def build_service_function_name(module_name: str, endpoint_name: str, method: str) -> str:
    return f"{method}_{module_name}_{endpoint_name}"


def build_service_function(
    module_name: str,
    endpoint_name: str,
    method: str,
    use_payload: bool = False,
) -> str:
    function_name = build_service_function_name(module_name, endpoint_name, method)

    if use_payload:
        return f"""
def {function_name}(payload):
    return {{"endpoint": "{endpoint_name}", "module": "{module_name}", "method": "{method}", "payload": payload.model_dump()}}
"""

    return f"""
def {function_name}():
    return {{"endpoint": "{endpoint_name}", "module": "{module_name}", "method": "{method}"}}
"""


def append_service_function(
    base_path: Path,
    module_name: str,
    endpoint_name: str,
    method: str,
    use_payload: bool = False,
) -> bool:
    service_file = base_path / "app" / module_name / "service.py"

    if not file_exists(service_file):
        raise FileNotFoundError(f'Arquivo de service não encontrado em app/{module_name}/service.py.')

    content = service_file.read_text(encoding="utf-8")
    function_name = build_service_function_name(module_name, endpoint_name, method)

    if f"def {function_name}(" in content:
        return False

    function_block = build_service_function(
        module_name=module_name,
        endpoint_name=endpoint_name,
        method=method,
        use_payload=use_payload,
    )

    new_content = content.rstrip() + "\n\n" + function_block.strip() + "\n"
    service_file.write_text(new_content, encoding="utf-8")

    return True