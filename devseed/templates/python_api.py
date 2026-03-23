README_TEMPLATE = """# {project_name}

Projeto Python backend criado com DevSeed.

## Como começar

### 1. Criar ambiente virtual
```bash
python -m venv .venv
```
### 2. Ativar ambiente virtual
**Windows**
```bash
.venv\\Scripts\\activate
```

**Linux/macOS**
```bash
source .venv/bin/activate
```
### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Rodar a aplicação
```bash
uvicorn app.main:app --reload
```
"""

MAIN_TEMPLATE = """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "DevSeed project running"}
"""

ENV_EXAMPLE_TEMPLATE = """APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000
"""

GITIGNORE_TEMPLATE = """.venv/
pycache/
*.pyc
.env
"""

REQUIREMENTS_TEMPLATE = """fastapi
uvicorn[standard]
pytest
httpx
"""

PYPROJECT_TEMPLATE = """[project]
name = "{project_name}"
version = "0.1.0"
description = "Projeto Python backend criado com DevSeed"
requires-python = ">=3.10"
"""