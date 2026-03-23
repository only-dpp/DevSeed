from pathlib import Path

from devseed.core.files import file_exists


def build_router_import(module_name: str) -> str:
    return f"from app.{module_name}.routes import router as {module_name}_router"


def build_router_include(module_name: str) -> str:
    return f'app.include_router({module_name}_router, prefix="/{module_name}", tags=["{module_name}"])'


def register_router_in_main(base_path: Path, module_name: str) -> bool:
    main_file = base_path / "app" / "main.py"

    if not file_exists(main_file):
        raise FileNotFoundError("app/main.py não encontrado.")

    content = main_file.read_text(encoding="utf-8")

    import_line = build_router_import(module_name)
    include_line = build_router_include(module_name)

    if import_line in content or include_line in content:
        return False

    lines = content.splitlines()

    import_insert_index = 0
    for index, line in enumerate(lines):
        if line.startswith("from ") or line.startswith("import "):
            import_insert_index = index + 1

    lines.insert(import_insert_index, import_line)

    app_line_index = None
    for index, line in enumerate(lines):
        if line.strip() == "app = FastAPI()":
            app_line_index = index
            break

    if app_line_index is None:
        raise ValueError("Não foi possível localizar 'app = FastAPI()' em app/main.py.")

    insert_index = app_line_index + 1

    while insert_index < len(lines) and lines[insert_index].strip() == "":
        insert_index += 1

    lines.insert(insert_index, "")
    lines.insert(insert_index + 1, include_line)

    main_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True