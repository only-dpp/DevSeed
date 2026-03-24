# DevSeed

![banner](/docs/devseed-banner.png)

![Python](https://img.shields.io/badge/python-3.13.12-3776AB?logo=python&logoColor=white)

CLI para criação e estruturação inicial de projetos backend em Python.

O DevSeed acelera o início do desenvolvimento, gerando uma base organizada com:
- estrutura de projeto
- módulos
- endpoints
- schemas
- services
- testes iniciais

---

## Motivação

Começar um projeto backend do zero geralmente envolve muita repetição:
- criar estrutura de pastas
- configurar ambiente
- montar rotas básicas
- escrever testes iniciais

O DevSeed resolve isso gerando uma base consistente em segundos.

---

## O que o DevSeed faz

- Cria estrutura inicial do projeto
- Configura ambiente (`.venv`, dependências)
- Gera módulos organizados
- Gera endpoints automaticamente
- Separa lógica em `routes`, `service` e `schemas`
- Cria testes iniciais automaticamente

---

## O que o DevSeed NÃO faz

O DevSeed não tenta ser um framework completo.

Ele:
- não acompanha automaticamente todas as mudanças do projeto
- não mantém testes sincronizados após alterações manuais
- não substitui o desenvolvimento do backend

Ele entrega uma base sólida. **A evolução do seu projeto é de sua responsabilidade.**

---

##  Instalação

clone o repositório
```bash
git clone https://github.com/only-dpp/DevSeed.git
```

instale o pacote em modo editável
```bash
pip install -e .
```

rode o --help:
```bash
devseed --help
```

caso seu python não esteja no path use:
```bash
python -m devseed --help
```

## Uso básico 

### 1. Criar projeto
```bash
devseed init nome-da-sua-api
cd nome da sua api
```

### 2. Preparar ambiente 
```bash
devseed setup
```

### 3. Rodar api
```bash
devseed run api
```

## Amostra do processo:
![init](/docs/iniciando%20api.png)


### Gerar módulo 
```bash
devseed generate module nome-do-modulo
```


### Gerar endpoint
```bash
devseed generate endpoint nome-do-modulo nome-do-endpoint --method post
```
isso gera automaticamente:
    rota
    service
    schemas(para métodos editaveis)
    teste

### Amostra do processo:
![generate](/docs/generate.png)


### Rodar testes
```bash
devseed run test
```

### Amostra do processo:
![run-test](/docs/run-test.png)

### Estrutura gerada
```bash
app/
    nome-do-seu-modulo/
        routes.py
        service.py
        schemas.py

tests/
    test_nome-do-seu-modulo.py
```


### Sobre os testes

Os testes gerados pelo DevSeed são iniciais e refletem a estrutura criada automaticamente por ele mesmo.
Depois de modificar o código gerado por ele, é esperado que os teste sejam ajustados pelo próprio desenvolvedor.

### Status do projeto

**Em desenvolvimento ativo**


### OBS:

O objetivo do DevSeed não é ser um copiloto para o desenvolvedor.
Ele apenas ajuda nas partes iniciais de um projeto.
Foi feito para ser uma ferramenta simples e pratica para:
    evitar começar do zero
    padronizar a estrutura inicial do seu código 
    acelerar o bootstrap de APIs 


### Contribuição

_contruibuições são muito bem-vindas :)_

## Licença
MIT
