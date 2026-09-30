# FiaBar — Guia para agentes

Controle de fiado para bares e comércios locais. Projeto da disciplina ESW442 (UniRV).

## Stack
- Python 3.12+
- Flask 3.x
- SQLite 3 (embutido no Python)
- pytest (testes) e ruff (lint)

## Comandos
- Criar ambiente: `python -m venv .venv`
- Ativar (Windows): `.venv\Scripts\activate`
- Ativar (Linux/Mac): `source .venv/bin/activate`
- Instalar: `pip install -r requirements.txt`
- Rodar: `flask --app app run`
- Testar: `pytest`
- Lint: `ruff check .`

## Estrutura
- `app/` — código da aplicação Flask
- `tests/` — testes pytest
- `docs/specs/` — specs das features (fonte da verdade)
- `docs/harness/` — relatórios do Better Harness e evidências

## Specs
Toda feature tem spec em `docs/specs/NNN-nome.md`. Critérios de aceite (CA-xx) e regras (RN-xx) da spec valem mais que qualquer suposição. Se algo não estiver na spec, pergunte antes de implementar.

## Como você deve trabalhar
1. **Pense antes de codar:** leia a spec, diga o que entendeu e aponte dúvidas antes de escrever código.
2. **Simplicidade primeiro:** escreva o mínimo que atende ao critério de aceite. Nada de funções fora do escopo da spec.
3. **Mudanças cirúrgicas:** altere só os arquivos necessários para a tarefa. Não reformate nem refatore código não relacionado.
4. **Guiado por verificação:** só considere uma tarefa pronta depois que `pytest` e `ruff check .` passarem, e mostre a saída.

## Segurança
- Nunca leia, edite ou exiba o arquivo `.env`.
- Nenhum servidor MCP instalado.
