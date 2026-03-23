from pathlib import Path

from devseed.core.files import file_exists


def build_endpoint_test_function(module_name: str, endpoint_name: str, http_method: str) -> str:
    function_name = f"test_{http_method}_{module_name}_{endpoint_name}"

    return f'''
def {function_name}():
    response = client.{http_method}("/{module_name}/{endpoint_name}")
    assert response.status_code == 200
    assert response.json() == {{"endpoint": "{endpoint_name}", "module": "{module_name}", "method": "{http_method}"}}
'''


def append_endpoint_test(
    base_path: Path,
    module_name: str,
    endpoint_name: str,
    http_method: str,
) -> bool:
    test_file = base_path / "tests" / f"test_{module_name}.py"

    if not file_exists(test_file):
        raise FileNotFoundError(f'Arquivo de teste não encontrado em tests/test_{module_name}.py.')

    content = test_file.read_text(encoding="utf-8")
    function_name = f"def test_{http_method}_{module_name}_{endpoint_name}():"

    if function_name in content:
        return False

    test_block = build_endpoint_test_function(module_name, endpoint_name, http_method)

    new_content = content.rstrip() + "\n\n" + test_block.strip() + "\n"
    test_file.write_text(new_content, encoding="utf-8")

    return True