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
- Declare suas suposições. Se o pedido admite duas leituras, pergunte antes de escolher uma.
- O mínimo que resolve. Sem abstração de uso único, sem opção que ninguém pediu, sem tratar erro que não acontece.
- Toque só no necessário. Mantenha o estilo do arquivo e não refatore código que funciona e não faz parte do pedido.
- Diga como vai provar que funcionou (`pytest` e `ruff check .`) e rode a prova antes de dizer que terminou.

## Segurança
- Nunca leia, edite ou exiba o arquivo `.env`.
- Nenhum servidor MCP instalado.
